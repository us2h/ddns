from utils.config import get_domains_from_file


class Validator:
    def __init__(self, config):
        self.config = config

    def validate(self):
        # Validate all necessary variables are set
        self.validate_config_set()
        # Validate provider specific variables are set
        self.validate_provider()

    def validate_config_set(self):
        # Check if provider is set
        if not self.config['PROVIDER']:
            # TODO: log error
            raise Exception('Provider not set')

        # Check if subdomains are set
        if not self.config['DOMAINS'] and not self.config['DOMAINS_FILE']:
            raise Exception('No domains set, please set DOMAINS or DOMAINS_FILE or both variables')

        # Check if subdomains file exists and is not empty if no other subdomains set
        if not self.config['DOMAINS'] and self.config['DOMAINS_FILE']:
            domains = get_domains_from_file(self.config['DOMAINS_FILE'])
            if not domains:
                raise Exception(f'File {self.config["DOMAINS_FILE"]} is empty or does not exist')

    def validate_variables(self, variables_list):
        missing_variables = []
        for variable in variables_list:
            if not self.config[variable]:
                missing_variables.append(variable)
        if missing_variables:
            raise Exception(f'Variables {missing_variables} are not set')
        return True

    def validate_provider(self):
        if self.config['PROVIDER'] == 'route53':
            self.validate_variables([
                'AWS_ACCESS_KEY_ID',
                'AWS_SECRET_ACCESS_KEY',
                'AWS_HOSTED_ZONE_ID',
            ])
