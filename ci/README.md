# Checkers

## Lints
- `bazel run //ci/lint:py_black -- --check $(pwd)/shortlist`
- `bazel run //ci/lint:py_flake8 -- $(pwd)/shortlist`

## Tests/Coverage for Django
- `bazel run //ci/testing:django -- --output_dir=$(pwd)`