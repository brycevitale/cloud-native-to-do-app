#!/bin/bash

# main deployment script for hw4
# this sets up the API VM, builds/pushes the frontend image,
# and deploys the frontend to kubernetes

PROJECT_ID="sound-catalyst-494222-q0"
ZONE="us-east1-b"
API_VM="cisc5550-api"
CLUSTER_NAME="cisc5550-cluster"
DOCKER_USER="brycevitale"
IMAGE_NAME="cisc5550todoapp"
DEPLOY_NAME="cc5550"

# use the right project and zone
gcloud config set project $PROJECT_ID
gcloud config set compute/zone $ZONE

# clean up old resources first if they exist
gcloud compute instances delete $API_VM --quiet
gcloud compute firewall-rules delete rule-allow-tcp-5001 --quiet
gcloud container clusters delete $CLUSTER_NAME --zone=$ZONE --quiet

# create the API VM
gcloud compute instances create $API_VM \
  --zone=$ZONE \
  --machine-type=e2-micro \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --tags=http-server \
  --metadata-from-file startup-script=./startup.sh

# open port 5001 for the API
gcloud compute firewall-rules create rule-allow-tcp-5001 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server \
  --allow tcp:5001

# copy my own API files over
gcloud compute scp todolist_api.py $API_VM:~/
gcloud compute scp todolist.db $API_VM:~/

# start the API app on the VM
# note: this keeps it running in the background after ssh exits
gcloud compute ssh $API_VM --command="nohup python3 todolist_api.py > api.log 2>&1 &"

# get the API VM's external IP
TODO_API_IP=$(gcloud compute instances list --filter="name=$API_VM" --format="value(EXTERNAL_IP)")

# build and push the frontend image for amd64 since GKE uses that
docker buildx build --platform linux/amd64 \
  -t $DOCKER_USER/$IMAGE_NAME:latest \
  --build-arg api_ip=$TODO_API_IP \
  --push .

# create the kubernetes cluster
gcloud container clusters create $CLUSTER_NAME --zone=$ZONE

# point kubectl at the cluster
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE

# deploy the frontend container
kubectl create deployment $DEPLOY_NAME --image=$DOCKER_USER/$IMAGE_NAME:latest --port=5000

# expose it publicly
kubectl expose deployment $DEPLOY_NAME --type=LoadBalancer --port=5000 --target-port=5000

# check the service
kubectl get service $DEPLOY_NAME
