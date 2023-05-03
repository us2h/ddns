import time
from config.common import APP_CONFIG
from validation import Validator
from ddns import DDNS

# Parse domains config
#subdomains = parse_domains_config(APP_CONFIG)


def loop():
    ddns = DDNS(provider_name=APP_CONFIG['PROVIDER'])
    while True:
        ddns.run()
        # Check again after predefined period
        time.sleep(APP_CONFIG['PERIOD'])


if __name__ == "__main__":
    # Validate config
    print('Validating config...')
    validator = Validator(APP_CONFIG)
    validator.validate()
    print('Config is valid')
    # Run loop
    try:
        print('Starting...')
        loop()
    except KeyboardInterrupt:
        print('Exiting...')
        exit()
