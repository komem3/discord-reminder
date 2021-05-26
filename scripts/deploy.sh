#!/bin/bash

set -ex

project=$1
token=$2

gcloud compute instances delete discord-reminder --zone=us-central1-a --quiet --project $project
gcloud compute instances create-with-container discord-reminder --zone=us-central1-a \
       --container-image "asia-northeast1-docker.pkg.dev/${project}/discord-reminder/reminder-bot" \
       --labels=env=dev --container-env="TOKEN=${token}" \
       --service-account="discord-bot@${project}.iam.gserviceaccount.com" \
       --machine-type=e2-micro \
       --scopes cloud-platform \
       --no-address \
       --preemptible --quiet --project $project
