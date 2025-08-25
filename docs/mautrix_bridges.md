



# Mautrix Bridge Integration

This guide explains how to integrate Mautrix bridges for Telegram and WhatsApp with Synapse.

## Overview

Instead of implementing custom bridges, we recommend using the well-maintained Mautrix bridge projects:

- [Mautrix Telegram](https://github.com/mautrix/telegram)
- [Mautrix WhatsApp](https://github.com/mautrix/whatsapp)

## Configuration

### 1. Telegram Bridge

Create `/data/appservices/telegram.yaml`:

```yaml
id: telegram
url: http://telegram-bridge:29328
as_token: "your-telegram-as-token"
hs_token: "your-telegram-hs-token"
sender_localpart: telegram_bot
namespaces:
  users:
    - exclusive: true
      regex: "@telegram_.*"
  aliases: []
  rooms: []
```

### 2. WhatsApp Bridge

Create `/data/appservices/whatsapp.yaml`:

```yaml
id: whatsapp
url: http://whatsapp-bridge:29328
as_token: "your-whatsapp-as-token"
hs_token: "your-whatsapp-hs-token"
sender_localpart: whatsapp_bot
namespaces:
  users:
    - exclusive: true
      regex: "@whatsapp_.*"
  aliases: []
  rooms: []
```

### 3. Docker Compose

Use the provided `docker-compose-with-mautrix-bridges.yml` to deploy Synapse with the bridges.

### 4. Environment Variables

Configure the following environment variables for the bridges:

**Telegram Bridge:**
- `MAUTRIX_TELEGRAM_API_ID`
- `MAUTRIX_TELEGRAM_API_HASH`
- `MAUTRIX_TELEGRAM_BOT_TOKEN`
- `MAUTRIX_TELEGRAM_HOMESERVER_URL`
- `MAUTRIX_TELEGRAM_APP_SERVICE_TOKEN`

**WhatsApp Bridge:**
- `MAUTRIX_WHATSAPP_HOMESERVER_URL`
- `MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN`

## Benefits of Using Mautrix Bridges

1. **Mature Implementation**: Battle-tested with large user bases
2. **Active Development**: Regular updates and bug fixes
3. **Full Feature Support**: Including media bridging, E2EE, and puppeting
4. **Community Support**: Large community and documentation

## Migration from Custom Bridges

If you were previously using custom bridge implementations, you can migrate to Mautrix bridges by:

1. Stopping your custom bridge services
2. Configuring the Mautrix bridges as shown above
3. Starting the Mautrix bridge containers
4. Verifying that messages are properly bridged

## Troubleshooting

- Check bridge logs for connection issues
- Verify that application service tokens match between Synapse and bridges
- Ensure proper DNS resolution between containers
- Check firewall settings for bridge containers



