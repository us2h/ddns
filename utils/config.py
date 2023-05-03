import os


def update_config_from_env(config: dict) -> dict:
    for key in config.keys():
        if key in os.environ:
            if isinstance(config[key], bool):
                if os.environ[key] in ['true', 'True']:
                    config[key] = True
                if os.environ[key] in ['false', 'False']:
                    config[key] = False
            else:
                config[key] = os.environ[key]
    return config


def get_domains_from_file(filename: str) -> list:
    try:
        with open(filename, 'r') as f:
            domains = f.readlines()
        return [domain.strip() for domain in domains]
    except FileNotFoundError:
        return []


def parse_domains_config(config: dict) -> list:
    domains = []

    if config['DOMAINS']:
        domains_from_variable = [
            domain.strip() for domain in config['DOMAINS'].split(',')
        ]
        domains.extend(domains_from_variable)

    if config['DOMAINS_FILE']:
        domains_from_file = get_domains_from_file(config['DOMAINS_FILE'])
        domains.extend(domains_from_file)

    return domains
