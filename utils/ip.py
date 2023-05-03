from requests import get


def get_current_ip(ipify_api_url):
    try:
        ip = get(ipify_api_url).text
    except Exception as e:
        # TODO: log error
        print(e)
        return None
    return ip
