import re
import requests
import json

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