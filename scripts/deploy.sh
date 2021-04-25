#!/bin/bash

project=$1
token=$2

gcloud compute instances delete discord-reminder --zone=us-central1-a --quiet
gcloud compute instances create-with-container discord-reminder --zone=us-central1-a \
       --container-image "gcr.io/${project}/reminder-bot" \
       --labels=env=dev --container-env="TOKEN=${token}" \
       --machine-type=e2-micro \
       --preemptible --project $project
