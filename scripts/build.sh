#!/bin/bash

set -ex

project=$1
gcloud builds submit \
       --quiet \
       --pack image="asia-northeast1-docker.pkg.dev/${project}/discord-reminder/reminder-bot" \
       --gcs-log-dir="gs://${project}-build-log/logs" \
       --project $project
