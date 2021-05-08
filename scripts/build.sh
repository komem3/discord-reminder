#!/bin/bash

set -x

project=$1
gcloud alpha builds submit --pack image="asia-northeast1-docker.pkg.dev/${project}/discord-reminder/reminder-bot" --quiet --project $project
