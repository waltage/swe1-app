import sys
from flake8.main.cli import main


if __name__ == "__main__":
  ret_code = main()
  sys.exit(ret_code)
