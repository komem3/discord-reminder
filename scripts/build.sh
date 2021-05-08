#!/bin/bash

set -x

project=$1
gcloud builds submit --quiet --pack image="asia-northeast1-docker.pkg.dev/${project}/discord-reminder/reminder-bot" --project $project
