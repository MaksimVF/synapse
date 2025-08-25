








#!/bin/bash
#
# Synapse Video Messenger Update Script
#
# This script updates the server to the latest version
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Synapse Video Messenger Update ===${NC}"

# Load environment variables
if [ -f /opt/synapse/.env ]; then
    source /opt/synapse/.env
else
    echo -e "${YELLOW}Environment file not found. Please create /opt/synapse/.env${NC}"
    exit 1
fi

# Backup current configuration
echo -e "${GREEN}Backing up configuration...${NC}"
cp /opt/synapse/.env /opt/synapse/.env.bak
cp -r /opt/synapse/config /opt/synapse/config.bak

# Update source code
echo -e "${GREEN}Updating source code...${NC}"
cd /opt/synapse/source
git pull origin neo
git checkout neo

# Copy new configuration files
echo -e "${GREEN}Updating configuration...${NC}"
cp -r docker/conf/* /opt/synapse/config/
cp docker/docker-compose-full-video.yml /opt/synapse/docker-compose.yml

# Restore custom configuration
cp /opt/synapse/.env.bak /opt/synapse/.env
cp -r /opt/synapse/config.bak/* /opt/synapse/config/

# Update services
echo -e "${GREEN}Updating services...${NC}"
cd /opt/synapse
docker-compose pull
docker-compose down
docker-compose up -d

# Clean up
echo -e "${GREEN}Cleaning up...${NC}"
docker image prune -f
docker volume prune -f

echo -e "${GREEN}Update completed!${NC}"
echo -e "${YELLOW}Your server has been updated to the latest version${NC}"



