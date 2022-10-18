load("@third_party//:requirements.bzl", "requirement")


def gen_3p(real, real_as=None):
  if not real_as:
    real_as = real

  native.py_library(
    name = real_as,
    deps = [
      requirement(real)
    ],
    visibility = [
      "//visibility:public"
    ]
  )

