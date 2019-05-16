#!/bin/sh
gcloud builds submit --tag gcr.io/risk-simulator-239019/risk-simulator
gcloud beta run deploy --image gcr.io/risk-simulator-239019/risk-simulator