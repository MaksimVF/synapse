












#!/bin/bash
#
# Synapse Video Messenger Monitoring Script
#
# This script checks the status of all services
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Synapse Video Messenger Status ===${NC}"

# Check Docker services
echo -e "${GREEN}Checking Docker services...${NC}"
cd /opt/synapse
SERVICES=$(docker-compose ps --services)

for SERVICE in $SERVICES; do
    STATUS=$(docker-compose ps -q $SERVICE | xargs docker inspect -f '{{.State.Status}}' 2>/dev/null || echo "not running")
    if [ "$STATUS" == "running" ]; then
        echo -e "  $SERVICE: ${GREEN}$STATUS${NC}"
    else
        echo -e "  $SERVICE: ${RED}$STATUS${NC}"
    fi
done

# Check disk space
echo -e "${GREEN}Checking disk space...${NC}"
df -h /opt/synapse | awk 'NR==2 {print "  Disk usage: " $5 " (" $4 " available)"}'

# Check memory usage
echo -e "${GREEN}Checking memory usage...${NC}"
free -h | awk 'NR==2 {print "  Memory: " $3 " used / " $2 " total"}'

# Check CPU load
echo -e "${GREEN}Checking CPU load...${NC}"
uptime | awk -F'load average:' '{print "  Load average: " $2}'

# Check logs for errors
echo -e "${GREEN}Checking logs for errors...${NC}"
ERRORS=$(docker-compose logs 2>&1 | grep -i "error\|fail\|crit" | wc -l)
if [ $ERRORS -gt 0 ]; then
    echo -e "  Found ${RED}$ERRORS${NC} error messages in logs"
else
    echo -e "  No errors found in logs"
fi

echo -e "${GREEN}Status check completed!${NC}"






