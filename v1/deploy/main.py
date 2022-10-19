from __future__ import annotations
import typing
import boto3
import json

APP_NAME = "django-hello"


APP_CONFIG = {
  "cluster": APP_NAME,
  "service": "{}-service".format(APP_NAME, ""),
}

BotoClient = boto3.session.Session.client

def get_cluster(client: BotoClient, app: str) -> typing.Tuple[bool, str]:
  clusters = client.list_clusters()
  for _ in clusters["clusterArns"]:
    if app in _:
      return True, _

  return False, ""

def get_services(client: BotoClient, cluster: str) -> typing.Tuple[bool, typing.List[str]]:
  services = client.list_services(
    cluster=cluster
  )
  if services["ResponseMetadata"]["HTTPStatusCode"] == 200:
    return True, services["serviceArns"]

  return False, []

def get_task_defs(client: BotoClient) -> typing.Tuple[bool, str]:
  task_defs = client.list_task_definitions()
  if task_defs["ResponseMetadata"]["HTTPStatusCode"] == 200:
    return True, task_defs["taskDefinitionArns"]
  return False, []




if __name__ == "__main__":

  client = boto3.client("ecs")

  ok, cluster = get_cluster(client, APP_NAME)
  ok, services = get_services(client, cluster)
  ok, task_defs = get_task_defs(client)
  for _ in task_defs:
    print(_)




def passit():

  result = client.describe_clusters(
    clusters=[cluster],
    include=[
      "ATTACHMENTS", "CONFIGURATIONS", "SETTINGS", "TAGS"
    ]
  )
