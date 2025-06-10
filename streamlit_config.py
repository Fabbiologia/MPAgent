"""Streamlit configuration settings."""

# Server configuration
PORT = 8501
ENABLE_CORS = False
ENABLE_XSRF = True
MAX_UPLOAD_SIZE = 200  # MB

# Browser configuration
SERVER_ADDRESS = '0.0.0.0'
BROWSER_SERVER_ADDRESS = '0.0.0.0'
BROWSER_GATHER_USAGE_STATS = True

# UI configuration
UI_HIDE_TOP_BAR = False
UI_HIDE_NAV = False
UI_HIDE_FOOTER = False

# Caching configuration
CLEAR_CACHE = False

# Logging configuration
LOG_LEVEL = 'info'
