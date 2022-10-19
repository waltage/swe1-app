from __future__ import annotations
import botocore
import boto3
import json
import typing


BotoClient = boto3.session.Session.client

from functions import _get_default_vpc
from functions import _get_subnets
from functions import _create_security_group
from functions import _update_ingress_rules
from functions import _create_load_balancer
from functions import _create_target_group
from functions import _create_listener


class DeployConfig:
  def __init__(self, app: str, region: str, tags: dict[str, str]):
    self.app = app
    self.region = region
    self.tags = tags

    self.ec2_client = boto3.client("ec2")
    self.elb_client = boto3.client("elbv2")

    self.sg_name = "{}-ext-sg".format(app)
    self.sg_desc = "automatic sg for app {}".format(app)
    self.lb_name = "{}-elb".format(app)
    self.tg_grp_name = "{}-elb-targets".format(app)

    self.vpc_id = _get_default_vpc(self.ec2_client)
    
    self.subnets = _get_subnets(self.ec2_client, self.vpc_id)

    self.sg_id = _create_security_group(
      self.ec2_client, 
      self.vpc_id,
      self.sg_name,
      self.sg_desc,
      self.tags
    )
    
    _update_ingress_rules(self.ec2_client, self.sg_id)

    lb_response = _create_load_balancer(
      self.elb_client, self.lb_name, self.subnets, self.sg_id, self.tags
    )
    self.lb_arn = lb_response["LoadBalancers"][0]["LoadBalancerArn"]
    self.tg_grp_arn = _create_target_group(
      self.elb_client,
      self.tg_grp_name,
      self.vpc_id,
      self.tags
    )

    self.listener = _create_listener(
      self.elb_client,
      self.lb_arn,
      self.tg_grp_arn,
      self.tags
    )

    # # get default vpc for logged in account
    # create a security group if none exists
    # update security group ingress rules if not set
    # create a load balancer with the security group if not exists
    # create a target group if not exists

    # create an ecs cluster if not exists
    # create an ecs task definition if not exists
    # create an ecs service if not exists
    # push the container as a task