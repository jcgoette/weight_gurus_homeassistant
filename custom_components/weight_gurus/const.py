"""weight_gurus constants."""
from __future__ import annotations

from datetime import timedelta
from logging import Logger, getLogger

# Base component constants
# TODO: allow to be overridden by config_flow
DATA_COORDINATOR_UPDATE_INTERVAL = timedelta(minutes=5)
DOMAIN = "weight_gurus"
NAME = "Weight Gurus"
VERSION = "v1.2.0"
LOGGER: Logger = getLogger(__package__)

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options

# Attributes
ATTR_ACTIVITY_LEVEL = "activityLevel"
ATTR_FIRST_NAME = "firstName"
ATTR_HEIGHT = "height"
ATTR_LAST_NAME = "lastName"
