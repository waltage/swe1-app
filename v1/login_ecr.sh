#!/bin/bash
echo "Logging in to ecr with docker"
source .env
echo ${SHORTLIST_ECR_REGISTRY}
aws ecr get-login-password --region ${SHORTLIST_ECR_REGION} | docker login --username AWS --password-stdin ${SHORTLIST_ECR_REGISTRY}
echo "Login complete."

# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 230664673572.dkr.ecr.us-east-1.amazonaws.com/nyu-swe1
# docker push 230664673572.dkr.ecr.us-east-1.amazonaws.com/nyu-swe1