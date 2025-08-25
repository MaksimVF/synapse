







#!/bin/bash
#
# Synapse Video Messenger Deployment Script
#
# This script deploys all services and configures the server
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Synapse Video Messenger Deployment ===${NC}"

# Load environment variables
if [ -f /opt/synapse/.env ]; then
    source /opt/synapse/.env
else
    echo -e "${YELLOW}Environment file not found. Please create /opt/synapse/.env${NC}"
    exit 1
fi

# Check for required variables
if [ -z "$SYNAPSE_SERVER_NAME" ]; then
    echo -e "${YELLOW}Please set SYNAPSE_SERVER_NAME in .env file${NC}"
    exit 1
fi

# Configure Nginx
echo -e "${GREEN}Configuring Nginx...${NC}"

cat > /etc/nginx/sites-available/synapse << EOF
server {
    listen 80;
    server_name $SYNAPSE_SERVER_NAME;

    # Synapse
    location /_matrix/ {
        proxy_pass http://127.0.0.1:8008;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Element Call
    location /call/ {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # LiveKit
    location /livekit/ {
        proxy_pass http://127.0.0.1:7880;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/synapse /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Get SSL certificate
echo -e "${GREEN}Getting SSL certificate...${NC}"
certbot --nginx -d $SYNAPSE_SERVER_NAME --non-interactive --agree-tos -m admin@$SYNAPSE_SERVER_NAME

# Start services
echo -e "${GREEN}Starting services...${NC}"
cd /opt/synapse
docker-compose pull
docker-compose up -d

# Configure firewall
echo -e "${GREEN}Configuring firewall...${NC}"
ufw allow 80
ufw allow 443
ufw allow 3478
ufw allow 3478/udp
ufw allow 5349
ufw allow 5349/udp
ufw allow 7880:7882/tcp
ufw allow 7882/udp
ufw reload

echo -e "${GREEN}Deployment completed!${NC}"
echo -e "${YELLOW}Your server is now running at https://$SYNAPSE_SERVER_NAME${NC}"
echo -e "${YELLOW}Element Call is available at https://$SYNAPSE_SERVER_NAME/call/${NC}"


