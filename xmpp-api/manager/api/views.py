# from services import communicationService, attackService, databaseService
from django.http import HttpResponse
from rest_framework.views import APIView, Response
import logging
import GetTemplate
import Service
import time
import datetime
import json
from django.core import serializers


# FILENAME = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M')) + ".log"
# FILENAME="meng.log"
# LOGFILE = "log/" + FILENAME
# logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(levelname)-8s %(message)s', filename=LOGFILE, filemode='w')
logger = logging.getLogger(__name__)
entry_counter = 0

# class TestList(APIView):
#     def get(self, request):
#         """
#         Returns all the tests in the database.
#         :param request: request
#         :return: JSON
#         """
#         return Response(databaseService.DatabaseService().get_all_tests())


# class ExecuteTest(APIView):
#     def get(self, request):
#         """
#         This get returns the configuration file which is specified in the header 'testname'
#         :param request:
#         :return:
#         """
#
#         return HttpResponse(communicationService.CommunicationService().get_configuration(
#             communicationService.CommunicationService().parseheaders(request)['TESTNAME']),
#             content_type="application/json")
#
#     def post(self, request):
#         """
#         Executes the test according with the configuration
#         supplied in the JSON
#         :param request: request
#         :return: True or False
#         """
#         logger.info("A new test is being executed.")
#         return Response(attackService.AttackService(request).response)

class CreatUsers(APIView):
    def post(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info("A new request of creating user")
        logger.info("the request body is: "+request.body)

        # print info
        # print Service.parseheaders(self, request)
        var = str(Service.gen_rand_str())
        res = [{"success":{"username": var}}]
        info = {"type": request.method, "header": Service.parseheaders(self, request), "reply":res, "url":request.path}
        print info
        # data = serializers.serialize('json',request.META)
        # for value in request.META:
        #     if "HTTP" in value:
        #         print "ADDED: " + value + " = " + request.META[value]
        # with open(LOGFILE,'w') as outfile:
        #     json.dump(data, outfile)
        return Response(res)
# class Redirector(APIView):
#     def get(self,request,suburl):
#         if suburl==


class GetAllInfo(APIView):
    def get(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: HttpRequest
        :return: JSON(replies all information of the "bridge")
        """
        # logger.info("Request of getting the information of the bridge")

        res = GetTemplate.get_complete_template()

        return Response(res)
    def post(self, request):
        """
        Return a JSON based on the post request
        :param request: HttpRequest
        :return: list of json(replies a valid "username" of the "bridge")
        """
        var = str(Service.gen_rand_str())
        res = [{"success":{"username": var}}]
        return Response(res)
class GetInfo(APIView):
    def get(self,request):
        res = GetTemplate.get_fake_info()
        return Response(res)

class SetLight(APIView):
    def put(self, request, light_id):
        """
        set the parameter of a light according to the light id and the content of request
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: JSON
        """
        # logger.info("Request of changing the the status of the light 1, body of the put request is: "+request.body)
        # return Response([{"lights": {}, "groups": {}}])
        res = GetTemplate.set_light(light_id, request)
        return Response(res)

class GetLight(APIView):
    def get(self, request, light_id):
        """
        get the information of one of the lights
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
                light_id: the id of the philips light
        :return: True or False
        """
        res = GetTemplate.get_light(light_id, request)
        # logger.info(json.dumps(infor))
        # info = {"type": request.method, "header": Service.parseheaders(self, request), "reply": res,
        #         "url": request.path}
        # print info
        # return Response([{"lights": {}, "groups": {}}])
        return Response(res)



class GetConfig(APIView):
    def get(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info(
            "GET Request of get the the info of the Config")
        #return Response([{"lights": {}, "groups": {}}])
        return Response(GetTemplate.get_config(request))
    def put(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info(
            "PUT Request of set the name of the bridge: " + request.body)
        # return Response([{"lights": {}, "groups": {}}])
        return Response(GetTemplate.set_config(request))


class GetSubInfo(APIView):
    def get(self, request, key):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        # logger.info(
        #     "GET Request of get the the info of the Config")
        res = GetTemplate.get_whatever(request,key)
        return Response(res)
    def put(self, request, key):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        return Response(GetTemplate.set_config(request,key))
class GetUsr(APIView):
    def get(self, request):
        res = GetTemplate.get_user()
        return Response(res)

class DelUsr(APIView):
    def delete(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        return Response(GetTemplate.err_msg(request))
