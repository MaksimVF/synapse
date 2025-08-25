



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
import requests
from typing import Any, Dict

from synapse.module_api import ModuleApi
from synapse.types import JsonDict

logger = logging.getLogger(__name__)

class LiveKitAuthModule:
    """Module to integrate LiveKit JWT authentication with Synapse"""

    @staticmethod
    def parse_config(config: JsonDict) -> Dict[str, Any]:
        """Parse the module configuration"""
        return {
            "lk_jwt_service_url": config.get("lk_jwt_service_url", "http://lk-jwt-service:8080"),
            "livekit_api_key": config.get("livekit_api_key", ""),
            "livekit_api_secret": config.get("livekit_api_secret", ""),
            "livekit_server_url": config.get("livekit_server_url", "http://livekit:7880"),
        }

    def __init__(self, config: Dict[str, Any], api: ModuleApi):
        self.api = api
        self.config = config

        # Register REST endpoint for LiveKit token generation
        self.api.register_rest_endpoint(
            path="/_synapse/client/livekit/token",
            method="GET",
            callback=self._generate_livekit_token,
        )

        logger.info("LiveKitAuthModule initialized with config: %s", config)

    async def _generate_livekit_token(
        self,
        request: "synapse.api.routes._base_base_servlets.BaseRequest",
    ) -> Dict[str, Any]:
        """Generate LiveKit JWT token"""
        user_id = request.user.to_string()

        # Call lk-jwt-service to generate token
        try:
            response = requests.post(
                f"{self.config['lk_jwt_service_url']}/generate",
                json={
                    "api_key": self.config["livekit_api_key"],
                    "api_secret": self.config["livekit_api_secret"],
                    "user_id": user_id,
                    "room_name": request.args.get("room_name", [""])[0],
                    "metadata": {
                        "display_name": request.args.get("display_name", [""])[0],
                    },
                },
                timeout=5,
            )
            response.raise_for_status()
            token_data = response.json()
            return {"token": token_data["token"]}

        except Exception as e:
            logger.error("Failed to generate LiveKit token: %s", e)
            raise Exception("Failed to generate LiveKit token") from e


