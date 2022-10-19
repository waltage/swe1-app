load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "8c8fe44ef0a9afc256d1e75ad5f448bb59b81aba149b8958f02f7b3a98f5d9b4",
    strip_prefix = "rules_python-0.13.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.13.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
     name = "python3_8",
     python_version = "3.8.12",
)

load("@rules_python//python:pip.bzl", "pip_parse")

load("@python3_8//:defs.bzl", "interpreter")
# Load 3P python requirements

pip_parse(
    name = "third_party_dep",
    python_interpreter_target = interpreter,
    requirements_lock = "//third_party:requirements.txt"
)

load("@third_party_dep//:requirements.bzl", "install_deps")
install_deps()