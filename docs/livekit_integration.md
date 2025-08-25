




# LiveKit Integration with Synapse

This guide explains how to integrate LiveKit with Synapse for WebRTC calls using the LiveKit JWT Authentication Service.

## Overview

LiveKit is a WebRTC SFU (Selective Forwarding Unit) that provides scalable video and audio conferencing. This integration allows Synapse users to make WebRTC calls using LiveKit infrastructure.

## Components

1. **LiveKit JWT Service**: Generates JWT tokens for LiveKit authentication
2. **LiveKit Proxy**: Handles token generation requests from Synapse
3. **Synapse Module**: Integrates LiveKit authentication with Synapse

## Setup

### 1. Deploy LiveKit JWT Service

Use the provided Docker Compose file to deploy the service:

```yaml
livekit-jwt-service:
  image: ghcr.io/element-hq/lk-jwt-service:latest
  environment:
    - LIVEKIT_API_KEY=your-livekit-api-key
    - LIVEKIT_API_SECRET=your-livekit-api-secret
    - JWT_EXPIRATION=24h
```

### 2. Configure Synapse Module

Add the LiveKit module to your Synapse configuration:

```yaml
modules:
  - module: "synapse.modules.livekit_auth.LiveKitAuthModule"
    config:
      lk_jwt_service_url: "http://livekit-jwt-service:8080"
      livekit_api_key: "your-livekit-api-key"
      livekit_api_secret: "your-livekit-api-secret"
```

### 3. Client Integration

Clients can request LiveKit tokens by calling the Synapse endpoint:

```http
GET /_synapse/client/livekit/token?room_name=my_room&display_name=My%20Name
```

The response will contain a JWT token that can be used to authenticate with LiveKit.

## Token Generation Flow

1. Client authenticates with Synapse
2. Client requests LiveKit token from Synapse
3. Synapse calls LiveKit JWT Service to generate token
4. Client receives token and connects to LiveKit

## Security Considerations

- Keep LiveKit API keys secure
- Use HTTPS for all communications
- Set appropriate token expiration times
- Validate user permissions before issuing tokens

## Troubleshooting

- Check LiveKit JWT Service logs
- Verify network connectivity between services
- Ensure proper CORS configuration
- Validate JWT tokens using LiveKit dashboard

## Benefits

1. **Scalable Calls**: LiveKit provides scalable WebRTC infrastructure
2. **Secure Authentication**: JWT-based authentication
3. **Easy Integration**: Simple REST API for token generation
4. **Flexible Configuration**: Customizable token parameters

## Resources

- [LiveKit Documentation](https://docs.livekit.io/)
- [LiveKit JWT Service](https://github.com/element-hq/lk-jwt-service)
- [Matrix WebRTC Specification](https://spec.matrix.org/latest/client-server-api/#voip)




