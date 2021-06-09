#!/usr/bin/env python
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

"""
Fetch a single file from a GitHub repository and write it to the current
directory, following LFS pointers to a custom LFS server if necessary.
"""

# The current implementation buffers everything in memory, so it may not be
# so great for truly huge files. But it takes < 2 seconds to grab an 11MB
# file, which is just fine for our typical use case.

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from hashlib import sha256
from pathlib import Path
from pprint import pprint
from urllib.parse import urlparse, urlunparse
import re
import requests


def url_concat(*pieces):
    return "/".join(piece.strip("/") for piece in pieces)


def main():
    parser = ArgumentParser(
        description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("org")
    parser.add_argument("repo")
    parser.add_argument("path")
    parser.add_argument(
        "--branch", default="main", help="The branch to fetch the file from"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show LFS server responses"
    )
    parser.add_argument(
        "--use-github-lfs-server",
        action="store_true",
        help="""
            This option isn’t as useful as it seems, because if the repo
            hasn’t exceed its quota, the usual ‘raw’ GitHub URL will return
            the LFS file directly.
        """,
    )
    # The LFS server could in theory be inferred by getting the repo’s
    # .lfsconfig file and parsing it.
    parser.add_argument(
        "--custom-lfs-server",
        default="https://lfs.altlab.dev",
        help="LFS server to use if necessary",
    )
    args = parser.parse_args()

    ## Get raw file from GitHub

    github_url = f"https://github.com/{args.org}/{args.repo}/raw/{args.branch}/{args.path}"
    print(f"Trying {github_url} …")
    github_response = requests.get(github_url)
    print(f"{github_response.status_code} {github_response.reason}")
    github_response.raise_for_status()

    out_file = Path(Path(args.path).name)

    if not github_response.content.startswith(
        b"version https://git-lfs.github.com/spec/v1\n"
    ):
        out_file.write_bytes(github_response.content)
        print(f"Wrote {out_file}.")
        return

    ## Ok, gotta use LFS.

    print("Got LFS pointer.")

    if args.debug:
        print(github_response.text)

    lfs_pointer_re = re.compile(
        r"""
        version\ https://git-lfs.github.com/spec/v1\n
        oid\ sha256:(?P<oid>[0-9a-f]{64})\n
        size\ (?P<size>[0-9]+)\n
    """,
        re.VERBOSE,
    )

    if not (match := lfs_pointer_re.fullmatch(github_response.text)):
        raise Exception("Unable to parse pointer file!")

    size = int(match["size"])

    ## Send a POST request with oid and size to get download href

    if args.use_github_lfs_server:
        lfs_url1 = url_concat(
            "https://github.com",
            args.org,
            args.repo.strip("/") + ".git",
            "info/lfs",
            "objects/batch",
        )
    else:
        lfs_url1 = url_concat(
            args.custom_lfs_server, args.org, args.repo, "objects/batch"
        )
    print(f"Trying {lfs_url1} …")
    lfs_response1 = requests.post(
        lfs_url1,
        headers={
            "Accept": "application/vnd.git-lfs+json",
            "Content-Type": "application/vnd.git-lfs+json",
        },
        json={
            "operation": "download",
            "transfers": ["basic"],
            "objects": [{"oid": match["oid"], "size": size}],
        },
    )
    print(f"{lfs_response1.status_code} {lfs_response1.reason}")
    if lfs_response1.status_code == 403:
        print(lfs_response1.text)
    lfs_response1.raise_for_status()

    lfs_info = lfs_response1.json()

    if args.debug:
        pprint(lfs_info)

    assert lfs_info["transfer"] == "basic"
    assert len(lfs_info["objects"]) == 1
    object_info = lfs_info["objects"][0]

    assert object_info["oid"] == match["oid"]
    assert object_info["size"] == size

    object_url = object_info["actions"]["download"]["href"]

    ## Time to download the actual file from the LFS server.

    # Display the URL, skipping any signatures in the query strings
    display_url_parts = urlparse(object_url)
    # There’s no easy way in the python stdlib to strip these out, so skip
    # printing the URL if they exist.
    if not display_url_parts.username and not display_url_parts.password:
        # `_replace` is a public method of namedtuple; “To prevent
        # conflicts with field names, the method and attribute names start
        # with an underscore.”
        display_url_parts = display_url_parts._replace(
            params="",
            query="" if not display_url_parts.query else "…",
            fragment="",
        )
        print(f"Trying {urlunparse(display_url_parts)} …")

    response = requests.get(object_url)
    print(f"{response.status_code} {response.reason}")
    response.raise_for_status()

    assert len(response.content) == size
    object_hash = sha256()
    object_hash.update(response.content)
    assert object_hash.hexdigest() == match["oid"]

    out_file.write_bytes(response.content)
    print(f"Wrote {out_file}.")


if __name__ == "__main__":
    main()
