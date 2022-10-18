import coverage





if __name__ == "__main__":
  cov = coverage.Coverage()
  cov.start()

  cov.stop()
  cov.save()
  cov.html_report()