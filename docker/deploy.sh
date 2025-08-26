


#!/bin/bash

# Synapse External Deployment Script
# This script helps deploy Synapse with external PostgreSQL, S3, and bridges

set -e

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Load environment variables
source .env

# Check required variables
REQUIRED_VARS=(
    SYNAPSE_SERVER_NAME
    SYNAPSE_TURN_SECRET
    POSTGRES_HOST
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_DB
    S3_BUCKET
    S3_REGION
    MAUTRIX_TELEGRAM_API_ID
    MAUTRIX_TELEGRAM_API_HASH
    MAUTRIX_TELEGRAM_BOT_TOKEN
    MAUTRIX_TELEGRAM_APP_SERVICE_TOKEN
    MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN
    LIVEKIT_API_KEY
    LIVEKIT_API_SECRET
)

for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        echo "Error: $VAR is not set in .env file"
        exit 1
    fi
done

# Create necessary directories
mkdir -p data
mkdir -p conf/appservices

# Update configuration files
echo "Updating configuration files..."

# Update homeserver-s3.yaml
sed -i "s/your.matrix.server/${SYNAPSE_SERVER_NAME}/g" conf/homeserver-s3.yaml
sed -i "s/your_secure_password/${POSTGRES_PASSWORD}/g" conf/homeserver-s3.yaml
sed -i "s/your.postgres.host/${POSTGRES_HOST}/g" conf/homeserver-s3.yaml
sed -i "s/your-s3-bucket-name/${S3_BUCKET}/g" conf/homeserver-s3.yaml
sed -i "s/your-aws-region/${S3_REGION}/g" conf/homeserver-s3.yaml

# Update appservice files
sed -i "s/your-telegram-as-token/${MAUTRIX_TELEGRAM_APP_SERVICE_TOKEN}/g" conf/appservices/telegram.yaml
sed -i "s/your-telegram-hs-token/${MAUTRIX_TELEGRAM_APP_SERVICE_TOKEN}/g" conf/appservices/telegram.yaml

sed -i "s/your-whatsapp-as-token/${MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN}/g" conf/appservices/whatsapp.yaml
sed -i "s/your-whatsapp-hs-token/${MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN}/g" conf/appservices/whatsapp.yaml

# Start services
echo "Starting Synapse with external services..."
docker-compose -f docker-compose-external.yml up -d

echo "Deployment completed successfully!"
echo ""
echo "Services available:"
echo "  - Synapse: http://${SYNAPSE_SERVER_NAME}:8008"
echo "  - Element Call: http://${SYNAPSE_SERVER_NAME}:8081"
echo "  - LiveKit: http://${SYNAPSE_SERVER_NAME}:7880"
echo ""
echo "To view logs: docker-compose -f docker-compose-external.yml logs -f"


