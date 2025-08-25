

# Enhanced Authentication Provider

The Enhanced Authentication Provider module extends Synapse's authentication capabilities to support multiple login methods including:

- Standard password authentication
- Phone number authentication
- OAuth/Social login integration

## Configuration

To enable the Enhanced Authentication Provider, add the following to your `homeserver.yaml`:

```yaml
modules:
  - module: "synapse.modules.auth_provider.EnhancedAuthProvider"
    config:
      enabled_login_types: ["password", "phone", "oauth"]
      oauth_providers:
        google:
          client_id: "your-google-client-id"
          client_secret: "your-google-client-secret"
        facebook:
          client_id: "your-facebook-client-id"
          client_secret: "your-facebook-client-secret"
        github:
          client_id: "your-github-client-id"
          client_secret: "your-github-client-secret"
```

## Authentication Methods

### Password Authentication

The module supports standard password authentication with the `m.login.password` login type.

### Phone Authentication

Phone authentication is supported via the `m.login.phone` login type. The module accepts phone numbers with country codes.

### OAuth Authentication

OAuth authentication is supported via the `m.login.oauth` login type. You can configure multiple OAuth providers.

## Auto-Registration

The module supports automatic user registration when a user successfully authenticates with a method but doesn't have a Matrix account yet.

## Implementation Details

The module implements the following callbacks:

- `auth_checkers`: For handling different authentication methods
- `check_3pid_auth`: For 3rd party identifier authentication
- `on_logged_out`: For handling user logout events

