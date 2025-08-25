









#!/bin/bash
#
# Synapse Video Messenger Backup Script
#
# This script creates a backup of the server configuration and data
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Synapse Video Messenger Backup ===${NC}"

# Create backup directory
BACKUP_DIR="/opt/synapse/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup configuration
echo -e "${GREEN}Backing up configuration...${NC}"
cp /opt/synapse/.env $BACKUP_DIR/
cp -r /opt/synapse/config $BACKUP_DIR/

# Backup database
echo -e "${GREEN}Backing up database...${NC}"
docker exec synapse-postgres pg_dump -U synapse -d synapse > $BACKUP_DIR/synapse_db.sql

# Backup media files
echo -e "${GREEN}Backing up media files...${NC}"
cp -r /opt/synapse/data/media_store $BACKUP_DIR/

# Create archive
echo -e "${GREEN}Creating backup archive...${NC}"
cd /opt/synapse/backups
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz $(basename $BACKUP_DIR)
rm -rf $BACKUP_DIR

echo -e "${GREEN}Backup completed!${NC}"
echo -e "${YELLOW}Backup saved to: /opt/synapse/backups/backup_$(date +%Y%m%d_%H%M%S).tar.gz${NC}"




