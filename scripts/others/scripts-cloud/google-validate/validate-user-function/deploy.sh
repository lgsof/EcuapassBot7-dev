gcloud functions deploy validate-user-function \
    --entry-point function \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated

