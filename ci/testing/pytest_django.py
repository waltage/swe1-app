import argparse
import coverage
import django
import os
import sys
import json
import requests
import subprocess

from django.conf import settings
from django.test.utils import get_runner

import hashlib
import datetime as dt

PARSER = argparse.ArgumentParser(description="Test with Coverage")
PARSER.add_argument("--output_dir", type=str, required=True)

if __name__ == "__main__":
  print(os.getcwd())
  args = PARSER.parse_args()
  cov_dir = os.path.join(args.output_dir, "coverage")
  data_file = os.path.join(cov_dir, ".coverage")
  lcov_file = os.path.join(cov_dir, "coverage.lcov")

  cov = coverage.Coverage(
    data_file=data_file,
    source_pkgs=[
      "shortlist",
      ],
    )
  cov.start()

  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shortlist.backend.hello.settings")
  django.setup()
  TestRunner = get_runner(settings)
  test_runner = TestRunner()

  fails = test_runner.run_tests(
    [ 
      "shortlist.backend.hello",
      "shortlist.backend.polls",
    ]
  )

  cov.stop()
  cov.save()
  cov.lcov_report(outfile=lcov_file)

  sys.exit(fails)