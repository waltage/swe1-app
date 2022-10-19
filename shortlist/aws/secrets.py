from __future__ import annotations

import boto3
import json

from typing import List


SHORTLIST_SECRET_ID = "prod/walt-nyu/projects"


class ShortlistSecretClient:
    def __init__(self, profile=None):
        self.profile = profile
        session = boto3.Session(profile_name=self.profile)
        self.client = session.client("secretsmanager")

    def get_secret(self, secret_id: str) -> str:
        secret = self.client.get_secret_value(SecretId=secret_id)
        return secret["SecretString"]

    def list_secrets(self) -> List[str]:
        all_secrets = self.client.list_secrets()
        results = []
        for _ in all_secrets["SecretList"]:
            results.append(_["Name"])
        return results

    def get_shortlist_config(self) -> dict[str, str]:
        secret_string = self.get_secret(SHORTLIST_SECRET_ID)
        obj = json.loads(secret_string)
        return obj
