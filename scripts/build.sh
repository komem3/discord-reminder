#!/bin/bash

project=$1
gcloud alpha builds submit --pack image="gcr.io/${project}/reminder-bot" --project $project
