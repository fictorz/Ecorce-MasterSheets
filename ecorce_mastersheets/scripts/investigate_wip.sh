#must be ran in powershell for now...

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
gcloud run services describe ecorce-mastersheets --region us-central1 --format='value(status.latestCreatedRevisionName)'
gcloud run services list --region us-central1