from config.common import APP_CONFIG
from utils.ip import get_current_ip
from utils.config import parse_domains_config


class DDNS:
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.domains = parse_domains_config(APP_CONFIG)
        self.last_ip_value = None

        # Initialize provider
        self._init_provider()

    def _init_provider(self):
        if self.provider_name == 'route53':
            # Import provider
            from providers.route53 import Route53
            # Initialize provider
            self.provider = Route53(
                access_key=APP_CONFIG['AWS_ACCESS_KEY_ID'],
                secret_key=APP_CONFIG['AWS_SECRET_ACCESS_KEY'],
                hosted_zone_id=APP_CONFIG['AWS_HOSTED_ZONE_ID'],
            )

    def run(self):
        # Get actual IP
        current_ip = get_current_ip(APP_CONFIG['IPIFY_URL'])
        if self.last_ip_value is None:
            # Set IP for the first time
            self.last_ip_value = current_ip
            # Check if domains are pointed to current IP
            domains_for_update = self._get_domains_for_update()
            print('Checking if domains are pointed to current IP...')
            print(f'Domains to check: {domains_for_update}')
            self._update_domains(domains_for_update, current_ip)

        # Check if IP has changed
        if current_ip != self.last_ip_value:
            # Update IP
            print('IP has changed, updating...')
            print(f'New IP: {current_ip}')
            print(f'Old IP: {self.last_ip_value}')
            self.last_ip_value = current_ip
            domains_for_update = self._get_domains_for_update()
            print(f'Domains for update: {domains_for_update}')
            self._update_domains(domains_for_update, current_ip)

    def _get_domains_for_update(self):
        for domain in self.domains:
            # Check if domain is wildcard
            if domain.startswith('*.'):
                # if domain is wildcard, get all subdomains
                subdomains = self._get_subdomains(domain)
                return subdomains
        # If no wildcard domains, return all domains
        return self.domains

    def _update_domains(self, domains, ip):
        for domain in domains:
            # Get actual record value
            actual_record_value = self._get_record_value(domain)
            if actual_record_value != ip:
                # Update record value
                print(f'Updating domain {domain} to {ip}')
                self._update_record_value(domain, ip)
            if actual_record_value == ip:
                print(f'Domain {domain} is already pointed to {ip}')

    def _get_subdomains(self, domain):
        return self.provider.get_resource_record_sets(domain)

    def _get_record_value(self, domain):
        actual_record_value = self.provider.get_record_value(domain)
        if actual_record_value is None:
            # TODO: log error
            return None
        return actual_record_value

    def _update_record_value(self, domain, ip):
        self.provider.update_record_value(domain, ip)
