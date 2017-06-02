import logging
from django.utils.deprecation import MiddlewareMixin
import api
import json
logger=logging.getLogger('middleware.middlewarelogrequest')
# import requests
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
        res = GetTemplate.get_complete_template()
        infor = api.Service.gen_json_log(self,request,res)
        logger.info(json.dumps(infor))
        return response