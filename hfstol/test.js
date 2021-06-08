const { Transducer } = require(".");
const { expect } = require("chai");
const { randomBytes } = require("crypto");

DEFAULT_TRANSDUCER_FILE = "../crk-relaxed-analyzer-for-dictionary.hfstol";

describe("hfstol-addon", function () {
  it("can look up atim", function () {
    const fst = new Transducer(DEFAULT_TRANSDUCER_FILE);
    expect(fst.lookup("atim")).to.deep.equal([
      "atim+N+A+Sg",
      "atimêw+V+TA+Imp+Imm+2Sg+3SgO",
    ]);
  });

  it("can look up itwêwina", function () {
    const fst = new Transducer(DEFAULT_TRANSDUCER_FILE);
    expect(fst.lookup("itwêwina")).to.deep.equal(["itwêwin+N+I+Pl"]);
  });

  it("returns nothing for invalid inputs", function () {
    const fst = new Transducer(DEFAULT_TRANSDUCER_FILE);
    expect(fst.lookup("avocado")).to.deep.equal([]);
  });

  it("throws an error if lookup() is passed invalid args", function () {
    const fst = new Transducer(DEFAULT_TRANSDUCER_FILE);
    expect(() => fst.lookup("abc", "def")).to.throw(Error, /argument/);
    expect(() => fst.lookup(123)).to.throw(Error, /string.*expected/);
  });

  it("throws an error if the transducer file doesn’t exist", function () {
    const nonExistentFile = randomBytes(30).toString("hex");
    expect(() => new Transducer(nonExistentFile)).to.throw(Error, /not found/);
  });
});
