#!/usr/bin/env python3
# type: ignore

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from argparse import ArgumentParser, BooleanOptionalAction, RawDescriptionHelpFormatter
from datetime import date, datetime
from pathlib import Path
from subprocess import check_call, check_output, CalledProcessError
from zoneinfo import ZoneInfo

import math
from setuptools.config import read_configuration

__doc__ = """
Release a python package, updating checked-in version number for development

When managing the version number of a package you maintain, do you find it
confusing to have the same version number checked in to the repository on
multiple commits, when that specific version number really only applies to the
single commit that actually gets released? But do you also not want to have to
update version numbers by hand?

This release script helps you get what you want through automation. It will use
`1.2.3.dev0` as the version number while you’re working on what will become
1.2.3. Then at release time it automatically creates a single tagged commit
where the checked-in version is `1.2.3`, and commits `1.2.4.dev0` as the new
version at HEAD for your continuing development work.

All it asks of you:
  - Add some notes to the “## Unreleased” section of `CHANGELOG.md` before
    releasing
  - If you want a major or minor version bump, commit the new development
    version, e.g., `2.3.0.dev0`, to `__VERSION__` at any time.
  - Make sure `setup.cfg` points at `file: my_python_package_name/__VERSION__`


The specific steps this script takes:
  - Remove .dev0 suffix from `__VERSION__`
  - Change “## Unreleased” to release version in `CHANGELOG.md`
  - Commit and tag
  - With optional --push flag: Push code with tag
  - With optional --release flag: Upload to pipi
  - Prepare for new development by updating CHANGELOG.md and setting
    `__VERSION__` to `n+1.dev0`

Note that since this is intended to be run in a temporary environment created by
some continuous integration system, on error it may leave the git working
directory in an unclean state.
"""


def main():
    try:
        default_git_branch = (
            check_output(["git", "branch", "--show-current"]).decode("UTF-8").strip()
        )
    except CalledProcessError as e:
        raise RuntimeError("Unable to determine default git branch name") from e

    parser = ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--push",
        action=BooleanOptionalAction,
        default=False,
        help="Push commits and tags",
    )
    parser.add_argument(
        "--release", action=BooleanOptionalAction, default=False, help="Upload release"
    )
    parser.add_argument(
        "--release-timezone",
        type=str,
        help="Timezone to calculate today’s date for changelog",
    )
    default_git_remote = "origin"
    parser.add_argument(
        "--git-remote",
        default=default_git_remote,
        help=f"Remote to push to (default: {default_git_remote})",
    )
    parser.add_argument(
        "--git-branch",
        default=default_git_branch,
        help=f"Branch  to push (default: {default_git_branch})",
    )
    parser.add_argument(
        "--use-github-actions-user-name-and-email", action=BooleanOptionalAction
    )
    parser.add_argument(
        "--git-user-name",
        type=str,
        help=f"Username to commit with",
    )
    parser.add_argument(
        "--git-user-email",
        type=str,
        help=f"Email to commit with",
    )

    def git_commit_env():
        ret = dict(os.environ)

        # If github-actions user specified, allow name or email to be overridden
        # by more specific arguments
        git_user = None
        git_email = None
        if args.use_github_actions_user_name_and_email:
            git_user = "github-actions"
            # https://api.github.com/users/github-actions%5Bbot%5D
            # https://github.community/t/github-actions-bot-email-address/17204/6
            git_email = "41898282+github-actions[bot]@users.noreply.github.com"
        if args.git_user_name is not None:
            git_user = args.git_user_name
        if args.git_user_email is not None:
            git_email = args.git_user_email

        if git_user is not None:
            ret.update(
                {
                    "GIT_AUTHOR_NAME": git_user,
                    "GIT_COMMITTER_NAME": git_user,
                }
            )
        if git_email is not None:
            ret.update(
                {
                    "GIT_AUTHOR_EMAIL": git_email,
                    "GIT_COMMITTER_EMAIL": git_email,
                }
            )

        if args.release_timezone:
            tz = ZoneInfo(args.release_timezone)
            dt = datetime.now(tz=tz)
            epoch_time = math.floor(dt.timestamp())
            tzoffset = dt.strftime("%z")
            git_time_str = f"{epoch_time} {tzoffset}"

            ret.update(
                {
                    "GIT_AUTHOR_DATE": git_time_str,
                    "GIT_COMMITTER_DATE": git_time_str,
                }
            )

        return ret

    args = parser.parse_args()

    # Versioning
    #
    # 0.0.3.dev0 ← version for all commits while working on v0.0.3
    # 0.0.3 ← version for *single* commit with tag python-v0.0.3, set by CI
    # 0.0.4.dev0 ← version in next commit
    #
    # https://www.python.org/dev/peps/pep-0440/#developmental-releases

    pypi_package_name: str = read_configuration("setup.cfg")["metadata"]["name"]
    python_package_name = pypi_package_name.replace("-", "_")

    version_file = Path(python_package_name) / "__VERSION__"
    current_dev_version: str = version_file.read_text().strip()
    release_version, new_dev_version = compute_new_versions(current_dev_version)

    bump_version_file(version_file, release_version)

    changelog_file = Path("CHANGELOG.md")
    changelog = Changelog(changelog_file.open("r+t"))

    if args.release_timezone:
        release_date = datetime.now(tz=ZoneInfo(args.release_timezone)).strftime(
            "%Y-%m-%d"
        )
    else:
        release_date = date.today()
    changelog.prepare_release(release_version, release_date)

    check_call(
        [
            "git",
            "commit",
            "-m",
            f"Release python v{release_version}",
            changelog_file,
            version_file,
        ],
        env=git_commit_env(),
    )
    check_call(["git", "tag", f"python-v{release_version}"])

    # The release commit is now created, but may only be pushed later if the
    # build succeeds

    build()

    release_file = Path("dist") / f"{pypi_package_name}-{release_version}.tar.gz"
    check_call(["twine", "check", "--strict", release_file])

    # We push before uploading the package. Ideally we could upload the package
    # and push the commit in the same transaction, but we are talking to very
    # different systems. In case something goes wrong, I think it’s much better
    # to have a commit that’s missing a release, or was manually released later,
    # than to have a release for which the commit was lost.
    push_cmd = [
        "git",
        "push",
        "--atomic",
        args.git_remote,
        args.git_branch,
        f"python-v{release_version}",
    ]

    if args.push:
        check_call(push_cmd)
    else:
        print(f"If --push was specified, would run {push_cmd!r}")

    release_cmd = ["twine", "upload", release_file]
    if args.release:
        check_call(release_cmd)
    else:
        print(f"If --release was specified, would run {release_cmd!r}")

    bump_version_file(version_file, new_dev_version)
    changelog.add_unreleased_section()

    check_call(
        [
            "git",
            "commit",
            "-m",
            f"Begin work on v{new_dev_version}",
            changelog_file,
            version_file,
        ],
        env=git_commit_env(),
    )

    push_cmd = [
        "git",
        "push",
        args.git_remote,
        args.git_branch,
    ]

    if args.push:
        check_call(push_cmd)
    else:
        print(f"If --push was specified, would run {push_cmd!r}")


def build():
    check_call(["python", "setup.py", "sdist"])


def compute_new_versions(current_dev_version):
    "Return (release_version, next_dev_version)"

    release_version = current_dev_version.removesuffix(".dev0")
    if release_version == current_dev_version:
        raise Exception(f"{current_dev_version} is not a dev version")

    pieces = list(map(int, release_version.split(".")))
    pieces[-1] = pieces[-1] + 1

    next_dev_version = ".".join(map(str, pieces)) + ".dev0"
    return (release_version, next_dev_version)


def bump_version_file(version_file: Path, new_version):
    version_file.write_text(new_version + '\n')

class Changelog:
    """
    This class automates several changelog lifecycle updates, as described under
    TEST_CHANGELOGS in the test source file.
    """

    def __init__(self, file_handle, filename="CHANGELOG.md"):
        """Create a changelog instance from an open file handle.

        The methods of this class will update that file *in place*.
        """
        self.filename = filename
        self.file_handle = file_handle
        self._parse()

    RE_HEADER = re.compile(
        r"^(##\s*(?:Unreleased$|v[0-9]+\.[0-9]+\.[0-9]+.*?)$)", flags=re.MULTILINE
    )
    RE_HEADER_UNRELEASED = re.compile(r"^##\s*Unreleased$")

    def add_unreleased_section(self):
        for i, piece in enumerate(self._pieces):
            if self.RE_HEADER.fullmatch(piece):
                # If there’s already an `## Unreleased` header, don’t add a new one
                if not self.RE_HEADER_UNRELEASED.fullmatch(piece):
                    self._pieces.insert(i, "## Unreleased\n\n")
                break
        else:
            raise ValueError(
                f"In {self.filename}, could not find existing release header before which to insert Unreleased header"
            )
        self._rewrite()

    def prepare_release(self, version, date):
        for i, piece in enumerate(self._pieces):
            if self.RE_HEADER_UNRELEASED.fullmatch(piece):
                if i >= len(self._pieces) or not self._pieces[i + 1].strip():
                    raise ValueError(
                        f"In {self.filename}, an Unreleased header was found, but its contents were empty"
                    )
                self._pieces[i] = f"## v{version} {date}"
                break
        else:
            raise ValueError(
                f"In {self.filename}, could not find Unreleased placeholder header to insert release info"
            )
        self._rewrite()

    def _parse(self):
        """Break the file into a list of (section header | body) text chunks

        Because of the `(...)` group enclosing RE_HEADER, the resulting list
        of pieces has the following properties:
          - ''.join(pieces) == original_text
          - each `piece` is either:
              - a section header, with self.RE_HEADER.fullmatch(piece) == True
              - or, raw non-header text between headers or at the start or end
                of the file
        """
        self.file_handle.seek(0)
        contents = self.file_handle.read()
        self._pieces = self.RE_HEADER.split(contents)

    def _rewrite(self):
        self.file_handle.seek(0)
        self.file_handle.write("".join(self._pieces))
        self.file_handle.truncate()
        self.file_handle.flush()


if __name__ == "__main__":
    main()
