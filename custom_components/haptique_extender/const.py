"""Constants for the Haptique Extender integration."""
from typing import Final

DOMAIN: Final = "haptique_extender"

# Configuration
CONF_INSTANCE_NAME: Final = "instance_name"

# Default values
DEFAULT_PORT: Final = 80
DEFAULT_SCAN_INTERVAL: Final = 10  # Poll every 10 seconds (no WebSocket)

# API Endpoints
API_STATUS: Final = "/api/status"
API_HOSTNAME: Final = "/api/hostname"
API_WIFI_STATUS: Final = "/api/wifi/status"
API_WIFI_WAIT: Final = "/api/wifi/wait"
API_WIFI_SCAN: Final = "/api/wifi/scan"
API_IR_SEND: Final = "/api/ir/send"
API_IR_LAST: Final = "/api/ir/last"
API_IR_TEST: Final = "/api/ir/test"
API_IR_RXINFO: Final = "/api/ir/rxinfo"
API_TOKEN: Final = "/api/token"
API_STORAGE_INFO: Final = "/api/storage/info"
API_AP_DISABLE: Final = "/api/ap/disable"

# IR Storage API Endpoints
API_IR_SAVE: Final = "/api/ir/save"
API_IR_SAVED: Final = "/api/ir/saved"
API_IR_SEND_NAME: Final = "/api/ir/send/name"
API_IR_DELETE: Final = "/api/ir/delete"
API_IR_CLEAR: Final = "/api/ir/clear"

# OTA API Endpoints
API_OTA_STATUS: Final = "/api/ota/status"
API_OTA_CONFIG: Final = "/api/ota/config"
API_OTA_MANIFEST: Final = "/api/ota/manifest"
API_OTA_CHECK: Final = "/api/ota/check"
API_OTA_URL: Final = "/api/ota/url"

# Challenge-Response Auth Endpoints
API_AUTH_CHALLENGE_SETUP: Final = "/api/auth/challenge/setup"
API_AUTH_CHALLENGE_GET: Final = "/api/auth/challenge/get"
API_AUTH_CHALLENGE_VERIFY: Final = "/api/auth/challenge/verify"
API_AUTH_CHALLENGE_STATUS: Final = "/api/auth/challenge/status"
API_AUTH_CHALLENGE_RESET: Final = "/api/auth/challenge/reset"

# Attributes
ATTR_FREQ_KHZ: Final = "freq_khz"
ATTR_DUTY: Final = "duty"
ATTR_REPEAT: Final = "repeat"
ATTR_RAW: Final = "raw"
