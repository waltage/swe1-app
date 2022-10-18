load("@third_party//:requirements.bzl", "requirement")


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
