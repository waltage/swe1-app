#!/bin/bash
echo "Building local version"
source .env
docker build -t ${ECR_REPO} .
echo "Built."
echo "Tagging"
docker tag ${ECR_REPO}:latest ${ECR_REGISTRY}/${ECR_REPO}:latest
echo "Tagged."
echo "Pushing"
docker push ${ECR_REGISTRY}/${ECR_REPO}:latest
echo "Pushed."