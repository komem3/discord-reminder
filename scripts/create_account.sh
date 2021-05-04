#!/bin/bash

project=$1

gcloud iam service-accounts create discord-bot --project $1

gcloud projects add-iam-policy-binding $project --member="serviceAccount:discord-bot@${project}.iam.gserviceaccount.com" --role=roles/artifactregistry.reader
gcloud projects add-iam-policy-binding $project --member="serviceAccount:discord-bot@${project}.iam.gserviceaccount.com" --role=roles/logging.logWriter
gcloud projects add-iam-policy-binding $project --member="serviceAccount:discord-bot@${project}.iam.gserviceaccount.com" --role=roles/monitoring.metricWriter	
gcloud projects add-iam-policy-binding $project --member="serviceAccount:discord-bot@${project}.iam.gserviceaccount.com" --role=roles/datastore.user		
