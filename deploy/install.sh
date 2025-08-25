






#!/bin/bash
#
# Synapse Video Messenger Installation Script
#
# This script sets up a complete video messaging server with:
# - Synapse (Matrix homeserver)
# - Element Call (video conferencing)
# - LiveKit (WebRTC backend)
# - Coturn (TURN/STUN server)
# - Telegram & WhatsApp bridges
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Synapse Video Messenger Installation ===${NC}"

# Check for root
if [ "$(id -u)" != "0" ]; then
    echo -e "${YELLOW}This script must be run as root${NC}"
    exit 1
fi

# Update system
echo -e "${GREEN}Updating system packages...${NC}"
apt-get update -qq && apt-get upgrade -y

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
apt-get install -y \
    docker.io \
    docker-compose \
    git \
    curl \
    jq \
    certbot \
    python3-certbot-nginx \
    nginx

# Enable services
systemctl enable docker
systemctl start docker

# Create directories
mkdir -p /opt/synapse
mkdir -p /opt/synapse/data
mkdir -p /opt/synapse/config
mkdir -p /opt/synapse/logs

# Clone repository
echo -e "${GREEN}Cloning Synapse repository...${NC}"
git clone https://github.com/MaksimVF/synapse.git /opt/synapse/source
cd /opt/synapse/source
git checkout neo

# Copy configuration files
echo -e "${GREEN}Setting up configuration...${NC}"
cp -r docker/conf/* /opt/synapse/config/
cp docker/docker-compose-full-video.yml /opt/synapse/docker-compose.yml

# Create environment file
cat > /opt/synapse/.env << EOF
# Synapse Configuration
SYNAPSE_SERVER_NAME=your.domain.com
SYNAPSE_TURN_SECRET=$(openssl rand -hex 16)

# LiveKit Configuration
LIVEKIT_API_KEY=$(openssl rand -hex 8)
LIVEKIT_API_SECRET=$(openssl rand -hex 16)

# Telegram Bridge
MAUTRIX_TELEGRAM_API_ID=your-telegram-api-id
MAUTRIX_TELEGRAM_API_HASH=your-telegram-api-hash
MAUTRIX_TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# WhatsApp Bridge
MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN=$(openssl rand -hex 16)
EOF

echo -e "${GREEN}Installation completed!${NC}"
echo -e "${YELLOW}Please edit /opt/synapse/.env with your configuration${NC}"
echo -e "${YELLOW}Then run: /opt/synapse/deploy.sh${NC}"


