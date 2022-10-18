from shortlist.aws.secrets import ShortlistSecretClient


if __name__ == "__main__":
  client = ShortlistSecretClient()
  conf = client.get_shortlist_config()

  print(conf)
  for k, v in conf.items():
    print(k, v)