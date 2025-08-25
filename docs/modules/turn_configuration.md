


# TURN Server Configuration Module

The TURN Configuration Module simplifies the setup of TURN servers for voice and video calls in Synapse.

## Configuration

To enable the TURN Configuration Module, add the following to your `homeserver.yaml`:

```yaml
modules:
  - module: "synapse.modules.turn_config.TurnConfigModule"
    config:
      turn_uris:
        - "turn:turn.example.com?transport=udp"
        - "turn:turn.example.com?transport=tcp"
      turn_shared_secret: "your-turn-secret"
      turn_user_lifetime: "1h"
      turn_allow_guests: true
```

## TURN Server Requirements

For voice and video calls to work properly, you need a TURN server with:

- Public IP address
- Open ports for UDP/TCP traffic (typically 3478, 5349)
- Proper firewall configuration

## Supported TURN Servers

The module works with any TURN server that supports the TURN REST API, including:

- coturn
- eturnal

## Implementation Details

The module configures the following Synapse settings:

- `turn_uris`: List of TURN server URIs
- `turn_shared_secret`: Shared secret for TURN authentication
- `turn_user_lifetime`: Lifetime of TURN credentials
- `turn_allow_guests`: Whether to allow guests to use TURN servers


