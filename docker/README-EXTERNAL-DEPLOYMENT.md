


# Synapse External Deployment Guide

This guide explains how to deploy Synapse with external PostgreSQL, S3 storage, Telegram/WhatsApp bridges, and video/audio call support.

## Features

- ✅ External PostgreSQL database
- ✅ S3 storage integration
- ✅ Telegram bridge
- ✅ WhatsApp bridge
- ✅ Video and audio calls with LiveKit
- ✅ TURN server for NAT traversal
- ✅ Element Call web client

## Prerequisites

1. **External PostgreSQL**: Set up a PostgreSQL cluster and create a database
2. **S3 Bucket**: Create an S3 bucket for media storage
3. **Domain**: Configure DNS for your Matrix server
4. **SSL**: Set up SSL certificates (via reverse proxy)
5. **API Keys**: Obtain API keys for Telegram, LiveKit, etc.

## Configuration

### 1. Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### 2. Update Configuration Files

Edit `conf/homeserver-s3.yaml` with your PostgreSQL and S3 credentials.

### 3. Bridge Configuration

Update the appservice files in `conf/appservices/` with your tokens.

## Deployment

### 1. Start Services

```bash
docker-compose -f docker-compose-external.yml up -d
```

### 2. Verify Services

Check logs to ensure all services are running:

```bash
docker-compose -f docker-compose-external.yml logs -f
```

### 3. Access Element Call

Open `http://your-server:8081` to access the video call client.

## External PostgreSQL Setup

### 1. Create Database

```sql
CREATE DATABASE synapse;
CREATE USER synapse_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE synapse TO synapse_user;
```

### 2. Configure Connection

Update `conf/homeserver-s3.yaml` with your PostgreSQL connection details:

```yaml
database:
  name: psycopg2
  args:
    user: synapse_user
    password: your_secure_password
    dbname: synapse
    host: your.postgres.host
    port: 5432
    cp_min: 5
    cp_max: 10
```

## S3 Storage Configuration

Update `conf/homeserver-s3.yaml` with your S3 bucket details:

```yaml
media_storage_providers:
  - module: s3_storage_provider.S3StorageProviderBackend
    store_local: true
    store_remote: true
    store_synchronous: true
    config:
      bucket: your-s3-bucket-name
      region_name: your-aws-region
      # Optional: specify credentials or use AWS default credential chain
      # access_key_id: your-access-key-id
      # secret_access_key: your-secret-access-key
```

## Telegram Bridge Setup

1. **Register Telegram App**: Go to https://my.telegram.org and create an application
2. **Update Environment**: Set these variables in `.env`:
   - `MAUTRIX_TELEGRAM_API_ID`
   - `MAUTRIX_TELEGRAM_API_HASH`
   - `MAUTRIX_TELEGRAM_BOT_TOKEN`
   - `MAUTRIX_TELEGRAM_APP_SERVICE_TOKEN`

3. **Update Appservice Config**: Edit `conf/appservices/telegram.yaml` with your tokens.

## WhatsApp Bridge Setup

1. **Update Environment**: Set this variable in `.env`:
   - `MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN`

2. **Update Appservice Config**: Edit `conf/appservices/whatsapp.yaml` with your tokens.

## Video/Audio Call Setup

1. **LiveKit Configuration**: Set these variables in `.env`:
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`

2. **TURN Server**: Configure with your domain and secret in `.env`:
   - `SYNAPSE_TURN_SECRET`

3. **DNS Configuration**: Set up these records:
   - `your.domain.com` (Synapse)
   - `turn.your.domain.com` (Coturn)
   - `livekit.your.domain.com` (LiveKit)

## Security Recommendations

1. **Use HTTPS**: Set up a reverse proxy (Nginx, Traefik) with SSL
2. **Firewall**: Restrict access to ports 8008, 8448, 3478, 5349, 7880-7882
3. **Monitoring**: Set up logging and monitoring for all services
4. **Backups**: Regularly backup your PostgreSQL database

## Troubleshooting

### 1. Database Connection Issues

- Check PostgreSQL firewall settings
- Verify credentials in `homeserver-s3.yaml`
- Check network connectivity

### 2. S3 Storage Issues

- Verify bucket permissions
- Check AWS credentials
- Test with a simple S3 upload

### 3. Bridge Connection Issues

- Verify appservice tokens match
- Check bridge logs
- Test connectivity between containers

### 4. Call Quality Issues

- Check TURN server connectivity
- Monitor LiveKit metrics
- Verify network conditions

## Maintenance

### 1. Updating Services

```bash
docker-compose -f docker-compose-external.yml pull
docker-compose -f docker-compose-external.yml up -d
```

### 2. Backups

Regularly backup:
- PostgreSQL database
- Synapse media store (if not using S3 exclusively)
- Configuration files

### 3. Monitoring

Set up monitoring for:
- Synapse performance
- PostgreSQL health
- S3 upload/download metrics
- Bridge connection status
- LiveKit call quality

## Support

For support, please contact your system administrator or open an issue in the repository.

