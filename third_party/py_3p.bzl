
load("@third_party//:requirements.bzl", "install_deps", "requirement")
install_deps()



def gen_3p(name, real_as=None):
  if not real_as:
    real_as = name

  native.py_library(
    name = real_as,
    deps = [
      requirement(name)
    ],
    visibility = [
      "//visibility:public"
    ]
  )

