# Checkers

## Lints
- `bazel run //ci/lint:py_black -- --check $(pwd)/shortlist`
- `bazel run //ci/lint:py_flake8 -- $(pwd)/shortlist`