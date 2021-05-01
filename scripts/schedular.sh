#!/bin/bash

project=$1

gcloud beta scheduler jobs create pubsub startup-dev-instances \
    --schedule '0 9 * * *' \
    --topic start-instance-event \
    --message-body '{"zone":"us-central1-a", "label":"env=dev"}' \
    --time-zone 'Asia/Tokyo' --project $project

gcloud beta scheduler jobs create pubsub shutdown-dev-instances \
    --schedule '0 1 * * *' \
    --topic stop-instance-event \
    --message-body '{"zone":"us-central1-a", "label":"env=dev"}' \
    --time-zone 'Asia/Tokyo' --project $project
