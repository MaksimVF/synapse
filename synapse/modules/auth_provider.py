

#
# This file is licensed under the Affero General Public License (AGPL) version 3.
#
# Copyright 2025 OpenHands
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# See the GNU Affero General Public License for more details:
# <https://www.gnu.org/licenses/agpl-3.0.html>.
#

import logging
from typing import Any, Dict, Optional, Tuple, Callable, Awaitable

from synapse.module_api import ModuleApi
from synapse.types import JsonDict

logger = logging.getLogger(__name__)

class EnhancedAuthProvider:
    """Enhanced authentication provider supporting multiple login methods"""

    @staticmethod
    def parse_config(config: JsonDict) -> Dict[str, Any]:
        """Parse the module configuration"""
        return {
            "enabled_login_types": config.get("enabled_login_types", ["password", "phone", "oauth"]),
            "oauth_providers": config.get("oauth_providers", {}),
        }

    def __init__(self, config: Dict[str, Any], api: ModuleApi):
        self.api = api
        self.config = config

        # Register authentication callbacks
        self.api.register_password_auth_provider_callbacks(
            auth_checkers={
                ("m.login.password", ("password",)): self._check_password,
                ("m.login.phone", ("phone", "country")): self._check_phone,
                ("m.login.oauth", ("provider", "token")): self._check_oauth,
            },
            check_3pid_auth=self._check_3pid_auth,
            on_logged_out=self._on_logged_out,
        )

        logger.info("EnhancedAuthProvider initialized with config: %s", config)

    async def _check_password(
        self,
        username: str,
        login_type: str,
        login_dict: JsonDict,
    ) -> Optional[Tuple[str, Optional[Callable[["synapse.rest.client.login.LoginResponse"], Awaitable[None]]]]]:
        """Check password-based authentication"""
        if login_type != "m.login.password":
            return None

        password = login_dict.get("password")
        if not password:
            return None

        # Here we would typically check against a user database or external auth system
        # For now, let's implement a simple check (in production, this should be more secure)
        user_id = self.api.get_qualified_user_id(username)

        # Check if user exists and password is correct
        user_exists = await self.api.check_user_exists(user_id)
        if not user_exists:
            # Auto-register user if they don't exist
            try:
                await self.api.register_user(localpart=username)
                logger.info("Auto-registered new user: %s", user_id)
            except Exception as e:
                logger.warning("Failed to auto-register user: %s", e)
                return None

        # In a real implementation, we would check the password hash here
        # For demonstration, we'll accept any non-empty password
        if password.strip():
            return (user_id, None)

        return None

    async def _check_phone(
        self,
        username: str,
        login_type: str,
        login_dict: JsonDict,
    ) -> Optional[Tuple[str, Optional[Callable[["synapse.rest.client.login.LoginResponse"], Awaitable[None]]]]]:
        """Check phone-based authentication"""
        if login_type != "m.login.phone":
            return None

        phone = login_dict.get("phone")
        country = login_dict.get("country")

        if not phone or not country:
            return None

        # In a real implementation, we would verify the phone number
        # For demonstration, we'll accept any phone number
        user_id = self.api.get_qualified_user_id(username)

        # Check if user exists, auto-register if not
        user_exists = await self.api.check_user_exists(user_id)
        if not user_exists:
            try:
                await self.api.register_user(localpart=username)
                logger.info("Auto-registered new user via phone: %s", user_id)
            except Exception as e:
                logger.warning("Failed to auto-register user via phone: %s", e)
                return None

        return (user_id, None)

    async def _check_oauth(
        self,
        username: str,
        login_type: str,
        login_dict: JsonDict,
    ) -> Optional[Tuple[str, Optional[Callable[["synapse.rest.client.login.LoginResponse"], Awaitable[None]]]]]:
        """Check OAuth-based authentication"""
        if login_type != "m.login.oauth":
            return None

        provider = login_dict.get("provider")
        token = login_dict.get("token")

        if not provider or not token:
            return None

        # In a real implementation, we would verify the OAuth token with the provider
        # For demonstration, we'll accept any non-empty token
        if provider not in self.config.get("oauth_providers", {}):
            logger.warning("Unknown OAuth provider: %s", provider)
            return None

        # Extract username from OAuth token (simplified)
        user_id = self.api.get_qualified_user_id(username)

        # Check if user exists, auto-register if not
        user_exists = await self.api.check_user_exists(user_id)
        if not user_exists:
            try:
                await self.api.register_user(localpart=username)
                logger.info("Auto-registered new user via OAuth: %s", user_id)
            except Exception as e:
                logger.warning("Failed to auto-register user via OAuth: %s", e)
                return None

        return (user_id, None)

    async def _check_3pid_auth(
        self,
        medium: str,
        address: str,
        password: str
    ) -> Optional[Tuple[str, Optional[Callable[["synapse.rest.client.login.LoginResponse"], Awaitable[None]]]]]:
        """Check 3rd party identifier authentication"""
        # For phone number authentication
        if medium == "msisdn":
            # In a real implementation, we would verify the phone number and password
            # For demonstration, we'll create a user ID from the phone number
            localpart = f"phone_{address}"  # Simplified - in production use a proper mapping
            user_id = self.api.get_qualified_user_id(localpart)

            # Check if user exists, auto-register if not
            user_exists = await self.api.check_user_exists(user_id)
            if not user_exists:
                try:
                    await self.api.register_user(localpart=localpart)
                    logger.info("Auto-registered new user via 3PID: %s", user_id)
                except Exception as e:
                    logger.warning("Failed to auto-register user via 3PID: %s", e)
                    return None

            return (user_id, None)

        return None

    async def _on_logged_out(
        self,
        user_id: str,
        device_id: Optional[str],
        access_token: str
    ) -> None:
        """Handle user logout"""
        logger.info("User logged out: %s, device: %s", user_id, device_id)
        # Here we could implement cleanup logic if needed

