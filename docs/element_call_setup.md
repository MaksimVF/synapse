





# Element Call Setup Guide

This guide explains how to set up and configure Element Call for video conferencing with Synapse.

## Overview

Element Call is a dedicated video conferencing application that integrates with Matrix for signaling and uses LiveKit for WebRTC infrastructure.

## Deployment

### 1. Docker Configuration

Element Call is included in the `docker-compose-full-video.yml` file:

```yaml
element-call:
  image: ghcr.io/element-hq/element-call:latest
  environment:
    - REACT_APP_DEFAULT_SERVER=https://your.domain.com
    - REACT_APP_DEFAULT_HS_URL=https://your.domain.com
    - REACT_APP_DEFAULT_IS_URL=https://your.domain.com
    - REACT_APP_LIVEKIT_URL=ws://livekit:7881
  ports:
    - "8081:80"
```

### 2. Configuration Options

#### Environment Variables

- `REACT_APP_DEFAULT_SERVER`: Matrix server URL
- `REACT_APP_DEFAULT_HS_URL`: Homeserver URL
- `REACT_APP_DEFAULT_IS_URL`: Identity server URL
- `REACT_APP_LIVEKIT_URL`: LiveKit WebSocket URL

#### Example Configuration

```env
REACT_APP_DEFAULT_SERVER=https://matrix.your.domain.com
REACT_APP_DEFAULT_HS_URL=https://matrix.your.domain.com
REACT_APP_DEFAULT_IS_URL=https://identity.your.domain.com
REACT_APP_LIVEKIT_URL=wss://livekit.your.domain.com:7881
```

### 3. Reverse Proxy Setup

Configure Nginx or Traefik to serve Element Call:

```nginx
server {
    listen 443 ssl;
    server_name call.your.domain.com;

    ssl_certificate /etc/letsencrypt/live/your.domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your.domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Features

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

## Integration with Element Web

To integrate Element Call with Element Web:

1. Add to `config.json`:

```json
{
  "livekit": {
    "url": "wss://livekit.your.domain.com:7881"
  }
}
```

2. Configure widgets:

```json
{
  "widgets": {
    "element-call": {
      "url": "https://call.your.domain.com",
      "name": "Element Call",
      "icon": "mxi:#icon"
    }
  }
}
```

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

- [Element Call GitHub](https://github.com/element-hq/element-call)
- [LiveKit Documentation](https://docs.livekit.io/)
- [Matrix VoIP Specification](https://spec.matrix.org/latest/client-server-api/#voip)





