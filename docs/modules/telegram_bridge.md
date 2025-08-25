



# Telegram Bridge Module

The Telegram Bridge Module provides integration between Matrix and Telegram messaging platforms.

## Configuration

To enable the Telegram Bridge Module, add the following to your `homeserver.yaml`:

```yaml
modules:
  - module: "synapse.modules.telegram_bridge.TelegramBridge"
    config:
      enabled: true
      api_id: "your-telegram-api-id"
      api_hash: "your-telegram-api-hash"
      bot_token: "your-telegram-bot-token"
      phone_number: "+1234567890"
```

## Features

- Bidirectional messaging between Matrix and Telegram
- Automatic room creation for Telegram chats
- User presence synchronization

## Implementation Details

The module implements the following callbacks:

- `check_event_for_spam`: To allow Telegram messages
- `user_may_join_room`: To allow Telegram users to join Matrix rooms

## Telegram API Requirements

You need to obtain Telegram API credentials:

1. Create a Telegram application at https://my.telegram.org
2. Get your API ID and hash
3. Create a bot and get the bot token

## Message Bridging

The module bridges messages in both directions:

- Matrix → Telegram: Messages sent in Matrix rooms are forwarded to Telegram
- Telegram → Matrix: Messages received from Telegram are forwarded to Matrix rooms



