from __future__ import annotations
import botocore
import boto3
import json

from typing import List


BotoClient = boto3.session.Session.client


def _tags_to_key_value(tags: dict[str, str]):
  return [{"Key": _[0], "Value": _[1]} for _ in tags.items()]


def _get_default_vpc(client: BotoClient) -> str:
  try:
      response = client.describe_vpcs()
      for _ in response["Vpcs"]:
        if _["IsDefault"]:
          return _["VpcId"]
      return ""
  except botocore.exceptions.ClientError as e:
    raise e


def _get_subnets(client: BotoClient, default_vpc: str) -> List[str]:
  try:
    response = client.describe_subnets(
        Filters=[{"Name": "vpc-id", "Values": [default_vpc]}]
      )
    return [_["SubnetId"] for _ in response["Subnets"]]
  except botocore.exceptions.ClientError as e:
    raise e


def _get_security_group_id(client: BotoClient, sg_name: str) -> str:
  real = client.describe_security_groups(
    Filters=[{"Name": "group-name","Values": [sg_name]}]
  )
  sgs = real["SecurityGroups"]
  if len(sgs) < 1:
    return ""
  return sgs[0]["GroupId"]


def _create_security_group(
    client: BotoClient, 
    vpc_id: str, 
    sg_name: str, 
    sg_desc: str, 
    tags: dict[str, str]) -> str:
  try:
    response = client.create_security_group(
        Description=sg_desc,
        GroupName=sg_name,
        VpcId=vpc_id,
        TagSpecifications=[
          {"ResourceType": "security-group", 
          "Tags": _tags_to_key_value(tags)
          }
        ]
      )
    return response["GroupId"]
  except botocore.exceptions.ClientError as e:
    if e.response["Error"]["Code"] == "InvalidGroup.Duplicate":
      return _get_security_group_id(client, sg_name)
    raise e

def _update_ingress_rules(client: BotoClient, sgid: str):
  try:
    response = client.authorize_security_group_ingress(
      GroupId=sgid,
      IpPermissions=[
        {
          "FromPort": 80,
          "IpProtocol": "TCP",
          "IpRanges": [
            {
              "CidrIp": "0.0.0.0/0",
              "Description": "allow all inbound"
            }
          ],
          "ToPort": 80,
        }
      ]
    )
  except botocore.exceptions.ClientError as e:
    if e.response["Error"]["Code"] == "InvalidPermission.Duplicate":
      return
    raise e


def _create_load_balancer(
    client: BotoClient, 
    lb_name: str, 
    subnets: List[str],
    sg_id: str,
    tags: dict[str, str]) -> str:
  try:
    response = client.create_load_balancer(
      Name=lb_name,
      Subnets=subnets,
      SecurityGroups=[
        sg_id
      ],
      Scheme="internet-facing",
      Tags=_tags_to_key_value(tags),
      Type="application",
      IpAddressType="ipv4"
    )
    return response
  except botocore.exceptions.ClientError as e:
    if e.response["Error"]["Code"] == "DuplicateLoadBalancerName":
      print(e.response)
      return
    raise e


def _create_target_group(
    client: BotoClient, 
    tg_grp_name: str, 
    vpc_id: str,
    tags: dict[str, str]):
  try:
    response = client.create_target_group(
      Name=tg_grp_name,
      Protocol="HTTP",
      Port=80,
      VpcId=vpc_id,
      HealthCheckProtocol="HTTP",
      HealthCheckPath="/health",
      TargetType="instance",
      Tags=_tags_to_key_value(tags),
      IpAddressType="ipv4"
    )
    return response["TargetGroups"][0]["TargetGroupArn"]
  except botocore.exceptions.ClientError as e:
    raise e


def _create_listener(
    client: BotoClient,
    lb_arn: str,
    tg_grp_arn: str,
    tags: dict[str, str]):
  response = client.create_listener(
    LoadBalancerArn=lb_arn,
    Protocol="HTTP",
    Port=80,
    DefaultActions=[
      {
        "Type": "forward",
        "TargetGroupArn": tg_grp_arn,
        "Order": 100,
      }
    ],
    Tags=_tags_to_key_value(tags)
  )
  return response