import re
import requests
import json
import datetime
import time
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

def gen_json_log(self, request, entry_counter, response):
    replytype = response._headers["content-type"][1]
    if 'json' in replytype:
        res = response.data
    else:
        res = response.content
    info = {"time": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S'),
            "entry_id": entry_counter, "type": request.method, "header": parseheaders(self, request),
            "reply_content": res, "reply_type": replytype ,"url": request.path, "body": request.body, "remote_ip": request.META['REMOTE_ADDR']}
    return info