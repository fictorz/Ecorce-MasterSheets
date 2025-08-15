gcloud run deploy ecorce-mastersheets ^
  --source . ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --memory=256Mi
  --set-build-env-vars="GOOGLE_PYTHON_VERSION=3.11"
