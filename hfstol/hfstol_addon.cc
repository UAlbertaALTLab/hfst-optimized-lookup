#include <napi.h>
#include "hfst-optimized-lookup.h"

#define VALUE_TO_CSTR(v) ((v).As<Napi::String>().Utf8Value().c_str())

/**
 * C++ node-addon-api wrapper for hfst-optimized-lookup
 *
 * Constructor: `new Transducer(path_to_hfstol_file)`
 * Methods:
 *     .lookup(string) => array of strings
 *         example: "atim" => ["atim+N+A+Sg", "atimêw+V+TA+Imp+Imm+2Sg+3SgO"]
 */
class TransducerWrapper : public Napi::ObjectWrap<TransducerWrapper> {

public:
  TransducerWrapper(const Napi::CallbackInfo &info)
      : Napi::ObjectWrap<TransducerWrapper>(info) {
    auto env = info.Env();

    if (info.Length() != 1) {
      Napi::TypeError::New(env, "Wrong number of arguments")
          .ThrowAsJavaScriptException();
      return;
    }

    try {
      tr = new TransducerFile(VALUE_TO_CSTR(info[0]));
    } catch (const std::exception &e) {
      throw Napi::Error::New(env, std::string(e.what()));
    }
  }

  Napi::Value lookup(const Napi::CallbackInfo &info) {
    auto env = info.Env();

    if (info.Length() != 1) {
      Napi::TypeError::New(env, "Wrong number of arguments")
          .ThrowAsJavaScriptException();
      return env.Null();
    }

    auto transducer_results = tr->lookup(VALUE_TO_CSTR(info[0]));

    auto ret = Napi::Array::New(env, transducer_results.size());
    for (size_t i = 0; i < transducer_results.size(); i++) {
      std::string results;
      for (auto const &value : transducer_results[i]) {
        results.append(value);
      }
      ret.Set((uint32_t)i, Napi::String::New(env, results));
    }
    return ret;
  }

private:
  TransducerFile *tr;
};

Napi::Object Init(Napi::Env env, Napi::Object exports) {
  Napi::Function transducerFile = TransducerWrapper::DefineClass(
      env, "Transducer",
      {TransducerWrapper::InstanceMethod("lookup",
                                         &TransducerWrapper::lookup)});

  exports.Set("Transducer", transducerFile);

  return exports;
}

NODE_API_MODULE(hfstol_addon, Init)
