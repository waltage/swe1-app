from __future__ import annotations

import argparse

from gunicorn.app.base import BaseApplication
from shortlist.backend.hello.wsgi import application


class ShortlistApp(BaseApplication):
  def __init__(self, app, options=None):
    self.options = options or {}
    self.application = app
    super().__init__()

  def load_config(self):
    for key, value in self.options.items():
      if key in self.cfg.settings and value:
        self.cfg.set(key, value)

  def load(self):
    return self.application

PARSER = argparse.ArgumentParser(description="Serve the django app")
PARSER.add_argument("--host", default="127.0.0.1", type=str)
PARSER.add_argument("--port", default=8000, type=int)
PARSER.add_argument("--workers", default=2, type=int)

if __name__ == "__main__":
  args = PARSER.parse_args()

  app = ShortlistApp(
    application,
    {
      "bind": "{}:{}".format(args.host, args.port),
      "workers": args.workers,
    }
  )

  app.run()