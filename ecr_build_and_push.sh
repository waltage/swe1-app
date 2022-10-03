#!/bin/bash
source .env

docker buildx build \
  --tag ${ECR_REGISTRY}/${ECR_REPO}:latest \
  --platform linux/amd64,linux/arm64 \
  --push .

aws ecr describe-images --repository-name=${ECR_REPO}