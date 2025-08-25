





# Video Calls Implementation

This guide explains how to set up video calls using Element Call, LiveKit, and Coturn with Synapse.

## Architecture

```
[Element Call] <--WebRTC--> [LiveKit] <--TURN--> [Coturn]
          |                           |
          v                           v
       [Synapse] <--Matrix--> [Bridges]
```

## Components

### 1. Element Call
- Web-based video call client
- Integrates with Matrix for signaling
- Uses LiveKit for WebRTC infrastructure

### 2. LiveKit
- WebRTC SFU (Selective Forwarding Unit)
- Handles media relay and processing
- Provides APIs for call management

### 3. Coturn
- TURN/STUN server for NAT traversal
- Required for P2P connections in restrictive networks

## Deployment

### 1. Configure Environment

Set these environment variables in `.env` file:

```env
# Synapse
SYNAPSE_SERVER_NAME=your.domain.com
SYNAPSE_TURN_SECRET=your-turn-secret

# LiveKit
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret

# Telegram Bridge
MAUTRIX_TELEGRAM_API_ID=your-telegram-api-id
MAUTRIX_TELEGRAM_API_HASH=your-telegram-api-hash
MAUTRIX_TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# WhatsApp Bridge
MAUTRIX_WHATSAPP_APP_SERVICE_TOKEN=your-whatsapp-as-token
```

### 2. Start Services

```bash
docker-compose -f docker-compose-full-video.yml up -d
```

### 3. Configure DNS

Set up DNS records for:
- `your.domain.com` (Synapse)
- `turn.your.domain.com` (Coturn)
- `livekit.your.domain.com` (LiveKit)

### 4. Configure SSL

Use a reverse proxy (Nginx, Traefik) with SSL termination.

## Client Configuration

### Element Call

Access Element Call at: `http://your-server:8081`

Configure with:
- Matrix Server: `https://your.domain.com`
- LiveKit URL: `ws://livekit.your.domain.com:7881`

### Element Web

For Element Web integration, add to `config.json`:

```json
{
  "livekit": {
    "url": "wss://livekit.your.domain.com:7881"
  }
}
```

## Call Features

### 1. One-to-One Calls
- Direct WebRTC connections
- Fallback to LiveKit SFU when needed

### 2. Group Calls
- Multi-party conferencing
- Screen sharing
- Recording

### 3. Mobile Support
- Works with Element iOS/Android apps
- Push notifications for incoming calls

## Security

### 1. Authentication
- JWT tokens for LiveKit access
- Matrix authentication for signaling

### 2. Encryption
- DTLS-SRTP for media
- HTTPS for signaling

### 3. Access Control
- Matrix room permissions
- Call moderation

## Troubleshooting

### 1. Call Quality Issues
- Check TURN server connectivity
- Monitor LiveKit metrics
- Verify network conditions

### 2. Connection Problems
- Check Coturn logs
- Verify TURN credentials
- Test STUN/TURN connectivity

### 3. Authentication Failures
- Verify JWT token generation
- Check LiveKit API keys
- Validate Matrix permissions

## Resources

- [Element Call Documentation](https://github.com/element-hq/element-call)
- [LiveKit Documentation](https://docs.livekit.io/)
- [Coturn Documentation](https://github.com/coturn/coturn)





