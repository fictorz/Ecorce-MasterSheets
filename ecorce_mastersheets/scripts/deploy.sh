#!/bin/bash

gcloud run deploy ecorce-mastersheets \
  --source ../ \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" \
  --memory=256Mi
  --set-build-env-vars="GOOGLE_PYTHON_VERSION=3.11"
