"""
db_config.py
-----------
Description:
   Database configuration settings for the Backend Service.
   Contains connection parameters for SQL Server instances.
   Configured for local development with multiple developer setups.

Author: Integration Service
Date: November 2025
"""

import os

# SQL Server Configuration
# Can be overridden by environment variables
DB_CONFIG = {
    'driver': os.environ.get('DB_DRIVER', 'SQL Server'),
    'server': os.environ.get('DB_SERVER', 'DESKTOP-824DEOL\\SQLEXPRESS01'),
    'database': os.environ.get('DB_DATABASE', 'AKINTOR'),
    'trusted_connection': os.environ.get('DB_TRUSTED_CONNECTION', 'yes')
}

# Alternative configurations for different developers
# Uncomment the configuration you need

# Karin's Configuration
# DB_CONFIG = {
#     'driver': 'SQL Server',
#     'server': 'OG-PROLECTS\\SQLEXPRESS',
#     'database': 'FinalProject',
#     'trusted_connection': 'yes'
# }

# Custom Configuration (can be set via environment variables)
# DB_DRIVER=SQL Server
# DB_SERVER=YOUR_SERVER\INSTANCE
# DB_DATABASE=YOUR_DATABASE
# DB_TRUSTED_CONNECTION=yes