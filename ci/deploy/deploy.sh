#!/bin/bash

(aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_DOCKER_REPO) || exit;
cd backend;
(docker build . \
  --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
  --build-arg BRANCH=main \
  --tag $AWS_DOCKER_REPO:latest) || exit;

(docker push $AWS_DOCKER_REPO:latest) || exit;
cd ..;


# set 0
echo "Reducing ECS capacity to 0..."
(aws ecs update-service --cluster $AWS_CLUSTER --service $AWS_SERVICE --desired-count 0 --no-paginate >/dev/null) || exit;
echo "    updated."
# stop current
tasks=$(aws ecs list-tasks --cluster $AWS_CLUSTER --service $AWS_SERVICE | grep -o -P '(arn.*[^"])')
echo $alltasks
while IFS= read -r task; do
  echo "Stopping: $task"
  (aws ecs stop-task --cluster $AWS_CLUSTER --task $task >/dev/null) || exit;
done <<< "$tasks"
echo "Stopped all tasks.  Waiting for new deployment."
sleep 5;
echo "Forcing new deployment..."
# force 1
(aws ecs update-service --cluster $AWS_CLUSTER --service $AWS_SERVICE --desired-count 1 --force-new-deployment >/dev/null) || exit;

DESIRED_ENDPOINT=http://lb-django-hello-516063654.us-east-1.elb.amazonaws.com/polls/

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' $DESIRED_ENDPOINT)" != "200" ]]; do 
  sleep 5
  echo "... waiting for 200"
done

echo "Deployment Completed."