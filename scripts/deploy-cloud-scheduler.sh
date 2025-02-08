#!/bin/sh

# Initialize variables
service_account_email=""
uri=""

# Parse named arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --sa=*)
            service_account_email="${1#*=}"
            ;;
        --uri=*)
            uri="${1#*=}"
            ;;
        *)
            echo "Invalid argument: $1"
            echo "Usage: $0 --sa=<service-account-email> --uri=<uri>"
            exit 1
            ;;
    esac
    shift
done

# Check if required arguments are provided
if [ -z "$service_account_email" ] || [ -z "$uri" ]; then
    echo "Both --sa and --uri arguments are required"
    echo "Usage: $0 --sa=<service-account-email> --uri=<uri>"
    exit 1
fi

gcloud scheduler jobs create http sc-demo-telegram-bot-scheduled \
  --location=europe-west3 \
  --schedule="0 * * * *" \
  --time-zone="Europe/Rome" \
  --uri="$uri" \
  --http-method=POST \
  --oidc-service-account-email="$service_account_email"