#!/bin/bash
echo "Logging in to ecr with docker"
source .env
aws ecr get-login-password --region ${SHORTLIST_ECR_REGION} | docker login --username AWS --password-stdin ${SHORTLIST_ECR_REGISTRY}
echo "Login complete."