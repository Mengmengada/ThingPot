import re
import requests
import json
import string, random
def parseheaders(self, request):
    """
    Method to parse the headers from the request because django requests are weird
    :param request:
    :return: Dict containing the headers
    """
    regex = re.compile('^HTTP_')
    headers = dict(
        (regex.sub('', header), value) for (header, value)
        in request.META.items() if header.startswith('HTTP_')
    )
    return headers

def gen_rand_str():
    ran_str = ''.join(random.choice(string.lowercase + string.digits + string.uppercase) for x in range(40))
    return ran_str