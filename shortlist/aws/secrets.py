import boto3


def connect():
  client = boto3.client("secretsmanager")
  return client