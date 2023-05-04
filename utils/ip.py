import ipaddress
from requests import get


def is_ipv4(string):
    try:
        ipaddress.IPv4Network(string)
        return True
    except ValueError:
        return False


def get_current_ip(ipify_api_url):
    try:
        ip = get(ipify_api_url).text
        if not is_ipv4(ip):
            return None
    except Exception as e:
        # TODO: log error
        print(e)
        return None
    return ip
