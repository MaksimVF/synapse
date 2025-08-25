


#
# This file is licensed under the Affero General Public License (AGPL) version 3.
#
# Copyright 2025 OpenHands
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# See the GNU Affero General Public License for more details:
# <https://www.gnu.org/licenses/agpl-3.0.html>.
#

import logging
from typing import Any, Dict

from synapse.module_api import ModuleApi
from synapse.types import JsonDict

logger = logging.getLogger(__name__)

class TurnConfigModule:
    """Module to configure TURN server for voice/video calls"""

    @staticmethod
    def parse_config(config: JsonDict) -> Dict[str, Any]:
        """Parse the module configuration"""
        return {
            "turn_uris": config.get("turn_uris", [
                "turn:turn.example.com?transport=udp",
                "turn:turn.example.com?transport=tcp"
            ]),
            "turn_shared_secret": config.get("turn_shared_secret", "default-secret"),
            "turn_user_lifetime": config.get("turn_user_lifetime", "1h"),
            "turn_allow_guests": config.get("turn_allow_guests", True),
        }

    def __init__(self, config: Dict[str, Any], api: ModuleApi):
        self.api = api
        self.config = config

        # Apply TURN configuration to the homeserver
        self._configure_turn()

        logger.info("TurnConfigModule initialized with config: %s", config)

    def _configure_turn(self) -> None:
        """Apply TURN configuration to the homeserver"""
        # This would typically be done through the homeserver configuration
        # For now, we'll log the configuration that should be applied
        logger.info("Configuring TURN server with URIs: %s", self.config["turn_uris"])
        logger.info("TURN shared secret: %s", self.config["turn_shared_secret"])
        logger.info("TURN user lifetime: %s", self.config["turn_user_lifetime"])
        logger.info("TURN allow guests: %s", self.config["turn_allow_guests"])

        # In a real implementation, we would update the homeserver's TURN configuration
        # For now, we'll just log a message indicating what should be configured
        logger.info(
            "To enable voice/video calls, add the following to your homeserver.yaml:\n"
            "turn_uris: %s\n"
            "turn_shared_secret: %s\n"
            "turn_user_lifetime: %s\n"
            "turn_allow_guests: %s",
            self.config["turn_uris"],
            self.config["turn_shared_secret"],
            self.config["turn_user_lifetime"],
            self.config["turn_allow_guests"]
        )

