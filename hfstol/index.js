'use strict';

const addon = require('bindings')('hfstol_addon');

const CppTransducer = addon.Transducer;

class Transducer extends CppTransducer {
  /**
   * Apply FST to text, returning array of analyses strings.
   *
   * E.g., lookup("atim") => ["atim+N+A+Sg", "atimêw+V+TA+Imp+Imm+2Sg+3SgO"]
   */
  lookup_symbols(text) {
    if (arguments.length !== 1) {
      throw new Error("Wrong number of arguments");
    }
    // Actual implementation is in C++
    return this._lookup_symbols(text);
  }

  /**
   * Apply FST to text, returning array of analyses strings.
   *
   * E.g., lookup("atim") => ["atim+N+A+Sg", "atimêw+V+TA+Imp+Imm+2Sg+3SgO"]
   */
  lookup(text) {
    if (arguments.length !== 1) {
      throw new Error("Wrong number of arguments");
    }

    const ret = [];
    for (const analysis of this.lookup_symbols(text)) {
      ret.push(analysis.join(""));
    }
    return ret;
  }

  /**
   * Apply FST to text, returning array of (1) array of prefix tags
   * (2) concatenated lemma and (3) array of suffix tags.
   *
   * E.g., lookup_lemma_with_affixes("kî-atimik")) ⇒
   *    [[["PV/ki"], "atimêw", ["+V", "+TA", "+Ind", "+4Sg/Pl", "+3SgO"]]]
   */
  lookup_lemma_with_affixes(text) {
    const ret = [];
    for (const analysis of this.lookup_symbols(text)) {
      const before = [];
      let beforeDone = false;
      let lemma = "";
      let lemmaDone = false;
      const after = [];

      for (const symbol of analysis) {
        if (symbol.length == 1) {
          // symbol is a character
          beforeDone = true;
          if (lemmaDone) {
            throw Exception("Unable to parse into lemma and affixes");
          }

          lemma += symbol;
        } else {
          // symbol is a tag
          if (!beforeDone) {
            before.push(symbol);
          } else {
            lemmaDone = true;
            after.push(symbol);
          }
        }
      }

      ret.push([before, lemma, after]);
    }
    return ret;
  }
}

module.exports = { Transducer };
