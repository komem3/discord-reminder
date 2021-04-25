#!/bin/bash

project=$1

gcloud compute instances delete discord-reminder --zone=us-central1-a
gcloud compute instances create-with-container discord-reminder --zone=us-central1-a \
    --container-image "gcr.io/${project}/reminder-bot" --preemptible --project $project
