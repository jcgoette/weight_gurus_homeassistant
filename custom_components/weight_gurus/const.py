"""weight_gurus constants."""
from __future__ import annotations

from datetime import timedelta
from logging import Logger, getLogger

# Base component constants
# TODO: allow to be overridden by config_flow
DATA_COORDINATOR_UPDATE_INTERVAL: timedelta = timedelta(minutes=5)
DOMAIN: str = "weight_gurus"
NAME: str = "Weight Gurus"
VERSION: str = "v1.2.0"
LOGGER: Logger = getLogger(__package__)

# Platforms
SENSOR: str = "sensor"
PLATFORMS: list = [SENSOR]

# Configuration and options

# Attributes
ATTR_ACTIVITY_LEVEL: str = "activityLevel"
ATTR_BMI: str = "bmi"
ATTR_BODY_FAT: str = "bodyFat"
ATTR_ENTRY_TIMESTAMP: str = "entryTimestamp"
ATTR_FIRST_NAME: str = "firstName"
ATTR_HEIGHT: str = "height"
ATTR_LAST_NAME: str = "lastName"
ATTR_MEASUREMENT: str = "measurement"
ATTR_MUSCLE_MASS: str = "muscleMass"
ATTR_WATER: str = "water"
ATTR_WEIGHT: str = "weight"
ATTR_KEYS: list = [ATTR_BMI, ATTR_BODY_FAT, ATTR_MUSCLE_MASS, ATTR_WATER, ATTR_WEIGHT]
