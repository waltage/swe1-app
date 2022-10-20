#!/bin/bash

AWS_DOCKER_REPO=230664673572.dkr.ecr.us-east-1.amazonaws.com/nyu-swe1
AWS_CLUSTER=django-hello
AWS_SERVICE=django-hello-web-service

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_DOCKER_REPO
docker build . \
  --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
  --build-arg BRANCH=deployment \
  --tag $AWS_DOCKER_REPO:latest

docker push .

# set 0
aws ecs update-service --cluster $AWS_CLUSTER --service $AWS_SERVICE --desired-count 0 --no-paginate >/dev/null

# stop current
tasks=$(aws ecs list-tasks --cluster $AWS_CLUSTER --service $AWS_SERVICE | grep -o -P '(arn.*[^"])')
echo $alltasks
while IFS= read -r task; do
  echo "Stopping: $task"
  aws ecs stop-task --cluster $AWS_CLUSTER --task $task >/dev/null
done <<< "$tasks"
# force 1
aws ecs update-service --cluster $AWS_CLUSTER --service $AWS_SERVICE --desired-count 1 --force-new-deployment >/dev/null