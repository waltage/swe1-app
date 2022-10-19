
load("@rules_python//python:defs.bzl", "py_library")
# load("@third_party//:requirements.bzl", "requirement")

def gen_3p(name, real_as=None):
  if not real_as:
    real_as = name

  py_library(
    name = real_as,
    deps = [
      "@third_party_{}//:pkg".format(real_as)
      # requirement(name)
    ],
    visibility = [
      "//visibility:public"
    ]
  )

