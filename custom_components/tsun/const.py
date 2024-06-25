"""Constants for TalentMonitor."""

# Base component constants
NAME = "TalentMonitor"
MANUFACTURER = "TSUNESS Co., Ltd."
DOMAIN = "tsun"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/stephanu/ha-talent-monitor/issues"


# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_CONNECTION_TALENT_MONITOR_CLOUD = "talent_monitor_cloud"
CONF_CONNECTION_TALENT_MONITOR_CLOUD_LABEL = "TALENT Monitoring and Management Portal"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
