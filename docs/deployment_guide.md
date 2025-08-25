






# Synapse Video Messenger Deployment Guide

This guide explains how to deploy the complete Synapse Video Messenger solution.

## Overview

This deployment includes:
- Synapse (Matrix homeserver)
- Element Call (video conferencing)
- LiveKit (WebRTC backend)
- Coturn (TURN/STUN server)
- Telegram & WhatsApp bridges

## Prerequisites

- Ubuntu 20.04/22.04 server
- Domain name with DNS configured
- Root access to the server

## Installation

### 1. Download the repository

```bash
git clone https://github.com/MaksimVF/synapse.git
cd synapse
git checkout neo
```

### 2. Copy deployment scripts

```bash
sudo cp -r deploy/ /opt/synapse/
sudo chmod +x /opt/synapse/deploy/*.sh
```

### 3. Run installation script

```bash
sudo /opt/synapse/deploy/install.sh
```

### 4. Edit configuration

Edit `/opt/synapse/.env` with your settings:

```env
SYNAPSE_SERVER_NAME=your.domain.com
SYNAPSE_TURN_SECRET=your-turn-secret
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
MAUTRIX_TELEGRAM_API_ID=your-telegram-api-id
MAUTRIX_TELEGRAM_API_HASH=your-telegram-api-hash
MAUTRIX_TELEGRAM_BOT_TOKEN=your-telegram-bot-token
MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN=your-whatsapp-as-token
```

## Deployment

### 1. Run deployment script

```bash
sudo /opt/synapse/deploy/deploy.sh
```

### 2. Access services

- **Synapse**: `https://your.domain.com`
- **Element Call**: `https://your.domain.com/call/`
- **LiveKit**: `https://your.domain.com/livekit/`

## Management

### Update

```bash
sudo /opt/synapse/deploy/update.sh
```

### Backup

```bash
sudo /opt/synapse/deploy/backup.sh
```

### Restore

```bash
sudo /opt/synapse/deploy/restore.sh backup_file.tar.gz
```

### Monitor

```bash
sudo /opt/synapse/deploy/monitor.sh
```

## Configuration

### Nginx

The deployment script configures Nginx with SSL. The configuration is available at `/etc/nginx/sites-available/synapse`.

### Docker Compose

The main configuration is in `/opt/synapse/docker-compose.yml`. You can customize services here.

## Troubleshooting

### 1. Check service status

```bash
sudo docker-compose -f /opt/synapse/docker-compose.yml ps
```

### 2. View logs

```bash
sudo docker-compose -f /opt/synapse/docker-compose.yml logs -f
```

### 3. Restart services

```bash
sudo docker-compose -f /opt/synapse/docker-compose.yml restart
```

## Security

### 1. Firewall

The deployment script configures UFW with necessary ports:

- 80, 443 (HTTP/HTTPS)
- 3478, 5349 (TURN/STUN)
- 7880-7882 (LiveKit)

### 2. SSL

Certbot is used to obtain SSL certificates automatically.

### 3. Backups

Regular backups are recommended. Use the backup script to automate this process.

## Resources

- [Synapse Documentation](https://matrix-org.github.io/synapse/latest/)
- [Element Call Documentation](https://github.com/element-hq/element-call)
- [LiveKit Documentation](https://docs.livekit.io/)
- [Coturn Documentation](https://github.com/coturn/coturn)





