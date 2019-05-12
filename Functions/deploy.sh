#!/bin/sh
gcloud functions deploy simulate --entry-point simulate_http --runtime python37 --trigger-http
