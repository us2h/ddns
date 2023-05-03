import boto3


class Route53:
    def __init__(self, access_key, secret_key, hosted_zone_id):
        self._access_key = access_key
        self._secret_key = secret_key
        self._hosted_zone_id = hosted_zone_id

        # Initialize connection
        self._init_connection()

    def _init_connection(self):
        # Try to connect to Route53
        try:
            self.route53_client = boto3.client(
                'route53',
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key,
            )
        # Catch invalid credentials
        except Exception as e:
            # TODO: log error
            raise e

    def _get_zone_id_by_domain(self, domain):
        response = self.route53_client.list_hosted_zones_by_name(
            DNSName=domain,
            MaxItems='1'
        )

        if (
                'HostedZones' in response.keys()
                and len(response['HostedZones']) > 0
                and response['HostedZones'][0]['Name'].startswith(domain)
        ):
            hosted_zone_id = response['HostedZones'][0]['Id'].split('/')[2]
            return hosted_zone_id
        else:
            return None

    def get_resource_record_sets(self, domain):
        subdomains = []

        response = self.route53_client.list_resource_record_sets(
            HostedZoneId=self._hosted_zone_id,
            StartRecordName=domain,
            StartRecordType='A',
        )
        for resource_record_set in response['ResourceRecordSets']:
            # TODO: Set necessary record types in config
            if resource_record_set['Type'] == 'A':
                subdomains.append({
                    'name': resource_record_set['Name'],
                    'value': resource_record_set['ResourceRecords'][0]['Value']
                })
        return subdomains

    # Get current IP from DNS record
    def get_record_value(self, domain):
        # Get DNS record
        response = self.route53_client.list_resource_record_sets(
            HostedZoneId=self._hosted_zone_id,
            StartRecordName=domain,
            StartRecordType='A',
            MaxItems='1',
        )

        # Parse response
        if (
                'ResourceRecordSets' in response.keys()
                and len(response['ResourceRecordSets']) > 0
                and response['ResourceRecordSets'][0]['Name'].startswith(domain)
        ):
            return response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
        else:
            return None

    # Update DNS record with new IP
    def update_record_value(self, domain, ip):
        # Update DNS record
        self.route53_client.change_resource_record_sets(
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain,
                            'ResourceRecords': [
                                {
                                    'Value': ip,
                                },
                            ],
                            'TTL': 60,
                            'Type': 'A',
                        },
                    },
                ],
                'Comment': 'Updated with ddns',
            },
            HostedZoneId=self._hosted_zone_id,
        )
