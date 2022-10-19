from __future__ import annotations
import typing
import boto3
import json

from deployment import DeployConfig
    

BotoClient = boto3.session.Session.client



def create_security_group(conf: DeployConfig):
  client = boto3.client("ec2")
  response = client.create_security_group(
    Description="automatic sg for app {}".format(conf.app),
    GroupName="{}-ext-sg".format(conf.app),
    VpcId=get_default_vpc(),
    TagSpecifications=[
      {
        "ResourceType": "security-group",
        "Tags": [
          
          {
            "Key": "nyu-project",
            "Value": conf.tag
          }
        ]
      }
    ]
  )

  sg_id = response["GroupId"]
  response2 = client.authorize_security_group_ingress(
    GroupId=sg_id,
    GroupName="{}-ext-sg".format(conf.app),
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

  return response2



def create_load_balancer(conf: DeployConfig):
  create_security_group(conf)
  client = boto3.client("elbv2")
  response = client.create_load_balancer(
    Name=conf.lb_name,
    Subnets=conf.subnets,
    SecurityGroups=[
      "{}-ext-sg".format(conf.app)
    ],
    Scheme="internet-facing",
    Tags=[
      {
        "Key": "nyu-project",
        "Value": conf.tag
      }
    ],
    Type="application",
    IpAddressType="ipv4",
  )
  return response




if __name__ == "__main__":

  config = DeployConfig(
    "django-second",
     "us-east-1",
     dict(nyu_project="hw1")
  )
  
  print(config.tg_grp_arn)
  print(config.listener)
  # client = boto3.client("ecs")

  # abc = create_security_group(config)

  # abc = create_load_balancer(config)
  # print(abc)

  # vpcs = get_default_vpc()
  # print(vpcs)
