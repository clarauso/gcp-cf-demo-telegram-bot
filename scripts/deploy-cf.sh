#!/bin/sh

run_service_account=""
api_key_secret=""

# Parse named arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --sa=*)
            run_service_account="${1#*=}"
            ;;
        --api-key-secret=*)
            api_key_secret="${1#*=}"
            ;;
        *)
            echo "Invalid argument: $1"
            echo "Usage: $0 --sa=<run-service-account-email> --api-key-secret=<api-key-secret>"
            exit 1
            ;;
    esac
    shift
done

# Check if required arguments are provided
if [ -z "$run_service_account" ] || [ -z "$api_key_secret" ]; then
    echo "Both --sa and --api-key-secret arguments are required"
    echo "Usage: $0 --sa=<run-service-account-email> --api-key-secret=<api-key-secret>"
    exit 1
fi

gcloud functions deploy cf-demo-telegram-bot-scheduled \
  --gen2 \
  --runtime=python312 \
  --region=europe-west8 \
  --source=src \
  --entry-point=send_message \
  --trigger-http \
  --set-secrets=TG_TOKEN="${api_key_secret}:latest" \
  --env-vars-file=gcp-env.yaml \
  --no-allow-unauthenticated \
  --concurrency=1 \
  --max-instances=1 \
  --ingress-settings=internal-only \
  --run-service-account="${run_service_account}"