import logging
from django.utils.deprecation import MiddlewareMixin
import Service
import json
import GetTemplate
logger=logging.getLogger('middleware.middlewarelogrequest')
# import requests
entry_counter = 0
class RequestLogging(MiddlewareMixin):

    def process_request(self,request):
        # logger.info(request)
        request._body_to_log = request.body
    def process_response(self,request,response):
        if not hasattr(request, '_body_to_log'):
            return response
        # msg = "path = %s"
        # args = request.path
        # logger.info(msg,*args)
        # print request.path + request._body_to_log
        global entry_counter
        entry_counter += 1
        infor = Service.gen_json_log(self,request,entry_counter,json.loads(response._container[0]))
        logger.info(json.dumps(infor))
        return response