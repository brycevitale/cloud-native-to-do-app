#!/bin/bash

# clean up cloud resources so they do not keep using credits

ZONE="us-east1-b"
API_VM="cisc5550-api"
CLUSTER_NAME="cisc5550-cluster"

gcloud compute instances delete $API_VM --quiet
gcloud compute firewall-rules delete rule-allow-tcp-5001 --quiet
gcloud container clusters delete $CLUSTER_NAME --zone=$ZONE --quiet
