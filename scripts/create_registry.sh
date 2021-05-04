#!/bin/bash

gcloud artifacts repositories create discord-reminder \
--repository-format=docker --location=asia-northeast1 --project $1

gcloud auth configure-docker asia-northeast1-docker.pkg.dev
