import argparse
import coverage
import django
import os

from django.conf import settings
from django.test.utils import get_runner

PARSER = argparse.ArgumentParser(description="Test with Coverage")
PARSER.add_argument("--output_dir", type=str, required=True)


if __name__ == "__main__":
  args = PARSER.parse_args()
  cov_dir = os.path.join(args.output_dir, "coverage")
  data_file = os.path.join(cov_dir, ".db")

  cov = coverage.Coverage(data_file=data_file)
  cov.start()

  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shortlist.backend.hello.settings")
  django.setup()
  TestRunner = get_runner(settings)
  test_runner = TestRunner()

  test_runner.run_tests(
    [ 
      "shortlist.backend.hello",
      "shortlist.backend.polls",
    ]
  )

  cov.stop()
  cov.save()
  print("covered: ", cov.html_report(directory=cov_dir))