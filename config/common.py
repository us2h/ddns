from utils.config import update_config_from_env

"""
Basic configuration
"""
APP_CONFIG = {
    # General
    # ---------
    # How often check for IP change
    'PERIOD': 60,
    # DNS provider
    'PROVIDER': 'route53',
    # In case if you want to use your own instance of ipify you can change this URL
    'IPIFY_URL': 'https://api.ipify.org',

    # Domains
    # ---------
    # Domains
    'DOMAINS': '',
    # File with domains list
    'DOMAINS_FILE': '',

    # Providers
    # ---------
    # Route53
    'AWS_ACCESS_KEY_ID': '',
    'AWS_SECRET_ACCESS_KEY': '',
    'AWS_HOSTED_ZONE_ID': '',
}

"""
If .env file exist and have keys also existing in this config then take values from .env file
"""
APP_CONFIG = update_config_from_env(APP_CONFIG)
