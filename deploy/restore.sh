











#!/bin/bash
#
# Synapse Video Messenger Restore Script
#
# This script restores the server from a backup
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Synapse Video Messenger Restore ===${NC}"

# Check for backup file
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: $0 <backup_file>${NC}"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f $BACKUP_FILE ]; then
    echo -e "${YELLOW}Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

# Stop services
echo -e "${GREEN}Stopping services...${NC}"
cd /opt/synapse
docker-compose down

# Extract backup
echo -e "${GREEN}Extracting backup...${NC}"
BACKUP_DIR="/opt/synapse/restore_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR
tar -xzf $BACKUP_FILE -C $BACKUP_DIR

# Restore configuration
echo -e "${GREEN}Restoring configuration...${NC}"
cp $BACKUP_DIR/*.env /opt/synapse/.env
cp -r $BACKUP_DIR/config/* /opt/synapse/config/

# Restore database
echo -e "${GREEN}Restoring database...${NC}"
cat $BACKUP_DIR/synapse_db.sql | docker exec -i synapse-postgres psql -U synapse -d synapse

# Restore media files
echo -e "${GREEN}Restoring media files...${NC}"
cp -r $BACKUP_DIR/media_store/* /opt/synapse/data/media_store/

# Start services
echo -e "${GREEN}Starting services...${NC}"
cd /opt/synapse
docker-compose up -d

# Clean up
echo -e "${GREEN}Cleaning up...${NC}"
rm -rf $BACKUP_DIR

echo -e "${GREEN}Restore completed!${NC}"
echo -e "${YELLOW}Your server has been restored from backup${NC}"





