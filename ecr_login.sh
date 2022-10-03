#!/bin/bash
echo "Logging in to ecr with docker"
source .env
aws ecr get-login-password --region ${ECR_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
echo "Login complete."