#!/bin/sh

service_account_email=""

while [ $# -gt 0 ]; do
    case "$1" in
        --sa=*)
            service_account_email="${1#*=}"
            ;;
        *)
            echo "Invalid argument: $1"
            echo "Usage: $0 --sa=<service-account-email>"
            exit 1
            ;;
    esac
    shift
done

gcloud functions add-invoker-policy-binding cf-demo-telegram-bot-scheduled \
      --region="europe-west8" \
      --member="serviceAccount:${service_account_email}"