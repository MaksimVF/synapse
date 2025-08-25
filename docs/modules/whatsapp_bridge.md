




# WhatsApp Bridge Module

The WhatsApp Bridge Module provides integration between Matrix and WhatsApp messaging platforms.

## Configuration

To enable the WhatsApp Bridge Module, add the following to your `homeserver.yaml`:

```yaml
modules:
  - module: "synapse.modules.whatsapp_bridge.WhatsAppBridge"
    config:
      enabled: true
      api_url: "https://api.whatsapp.com"
      api_key: "your-whatsapp-api-key"
      phone_number: "+1234567890"
```

## Features

- Bidirectional messaging between Matrix and WhatsApp
- Automatic room creation for WhatsApp chats
- User presence synchronization

## Implementation Details

The module implements the following callbacks:

- `check_event_for_spam`: To allow WhatsApp messages
- `user_may_join_room`: To allow WhatsApp users to join Matrix rooms

## WhatsApp API Requirements

You need to obtain WhatsApp API credentials:

1. Apply for WhatsApp Business API access
2. Get your API key and phone number

## Message Bridging

The module bridges messages in both directions:

- Matrix → WhatsApp: Messages sent in Matrix rooms are forwarded to WhatsApp
- WhatsApp → Matrix: Messages received from WhatsApp are forwarded to Matrix rooms




