const { Transducer } = require('.');
const { expect } = require('chai');
const { randomBytes } = require('crypto');

const DEFAULT_TRANSDUCER_FILE = "../crk-relaxed-analyzer-for-dictionary.hfstol";

describe("hfstol-addon", function () {
  describe("with the Plains Cree FST", function () {
    let fst;
    before(() => {
      fst = new Transducer(DEFAULT_TRANSDUCER_FILE);
    });

    it("can look up atim", function () {
      expect(fst.lookup("atim")).to.deep.equal([
        "atim+N+A+Sg",
        "atimêw+V+TA+Imp+Imm+2Sg+3SgO",
      ]);
    });

    it("can look up itwêwina", function () {
      expect(fst.lookup("itwêwina")).to.deep.equal(["itwêwin+N+I+Pl"]);
    });

    it("can look up symbols for atim", function () {
      expect(fst.lookup_symbols("atim")).to.deep.equal([
        ["a", "t", "i", "m", "+N", "+A", "+Sg"],
        [
          "a",
          "t",
          "i",
          "m",
          "ê",
          "w",
          "+V",
          "+TA",
          "+Imp",
          "+Imm",
          "+2Sg",
          "+3SgO",
        ],
      ]);
    });

    it("can look up lemma with affixes for atim", function () {
      expect(fst.lookup_lemma_with_affixes("atim")).to.deep.equal([
        [[], "atim", ["+N", "+A", "+Sg"]],
        [[], "atimêw", ["+V", "+TA", "+Imp", "+Imm", "+2Sg", "+3SgO"]],
      ]);
    });

    it("can look up lemma with affixes for kî-atimik", function () {
      expect(fst.lookup_lemma_with_affixes("kî-atimik")).to.deep.equal([
        [["PV/ki+"], "atimêw", ["+V", "+TA", "+Ind", "+4Sg/Pl", "+3SgO"]],
      ]);
    });

    it("returns nothing for invalid inputs", function () {
      expect(fst.lookup("avocado")).to.deep.equal([]);
    });

    it("throws an error if lookup() is passed invalid args", function () {
      expect(() => fst.lookup("abc", "def")).to.throw(Error, /argument/);
      expect(() => fst.lookup(123)).to.throw(Error, /string.*expected/);
    });
  });

  it("throws an error if the transducer file doesn’t exist", function () {
    const nonExistentFile = randomBytes(30).toString("hex");
    expect(() => new Transducer(nonExistentFile)).to.throw(Error, /not found/);
  });
});
