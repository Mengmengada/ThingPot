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
FILENAME="meng.log"
LOGFILE = "log/" + FILENAME
logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s', filename=LOGFILE, filemode='w')
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
        # return Response(Service.parseheaders(self, request))
        # return Response(request)
class GetAllInfo(APIView):
    def get(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        global entry_counter
        entry_counter += 1
        logger.info("Request of getting the information of the bridge")
        res = GetTemplate.get_complete_template()
        info = {"entry_id": entry_counter, "type": request.method, "header": Service.parseheaders(self, request), "reply": res,
                "url": request.path}
        logger.info(json.dumps(info))
        # return Response([{"lights": {}, "groups": {}}])
        return Response(res)

class SetLight2(APIView):
    def put(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info("Request of changing the the status of the light 2, body of the put request is: " + request.body)
        # return Response([{"lights": {}, "groups": {}}])
        return Response(GetTemplate.set_light(2,request))

class SetLight1(APIView):
    def put(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info("Request of changing the the status of the light 1, body of the put request is: "+request.body)
        # return Response([{"lights": {}, "groups": {}}])
        return Response(GetTemplate.set_light(1, request))
class SetLight(APIView):
    def put(self, request, light_id):
        """
        set the parameter of a light according to the light id and the content of request
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info("Request of changing the the status of the light 1, body of the put request is: "+request.body)
        # return Response([{"lights": {}, "groups": {}}])
        return Response(GetTemplate.set_light(light_id, request))

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
        logger.info(
            "GET Request of get the the info of the light " + light_id)
        res = GetTemplate.get_light(light_id, request)
        info = {"type": request.method, "header": Service.parseheaders(self, request), "reply": res,
                "url": request.path}
        print info
        # return Response([{"lights": {}, "groups": {}}])
        return Response(res)

# class GetLight1(APIView):
#     def get(self, request):
#         """
#         Executes the test according with the configuration
#         supplied in the JSON
#         :param request: request
#         :return: True or False
#         """
#         logger.info(
#             "GET Request of get the the info of the light 1")
#         # return Response([{"lights": {}, "groups": {}}])
#         return Response(GetTemplate.get_light(1, request))
#
# class GetLight2(APIView):
#     def get(self, request):
#         """
#         Executes the test according with the configuration
#         supplied in the JSON
#         :param request: request
#         :return: True or False
#         """
#         logger.info(
#             "GET Request of get the the info of the light 2")
#         # return Response([{"lights": {}, "groups": {}}])
#         return Response(GetTemplate.get_light(2, request))

class GetLights(APIView):
    def get(self, request):
        """
        get information of a group of lights
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info(
            "GET Request of get the the info of the lights : " + request.body)
        res = GetTemplate.get_light(None, request)
        info = {"type": request.method, "header": Service.parseheaders(self, request), "reply": res,
                "url": request.path}
        print info
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
        logger.info(
            "GET Request of get the the info of the Config")
        #return Response([{"lights": {}, "groups": {}}])
        return Response(GetTemplate.get_whatever(request,key))

class DelUsr(APIView):
    def delete(self, request):
        """
        Executes the test according with the configuration
        supplied in the JSON
        :param request: request
        :return: True or False
        """
        logger.info(
            "DELETE Request to delete user in whitelist")
        # return Response([{"lights": {}, "groups": {}}])
        return Response(GetTemplate.err_msg(request))


# class TestPost(APIView):
#     def post(self, request):
#         """
#         Used for seeing the request
#         :param request: request
#         :return: Dict
#         """
#         test = communicationService.CommunicationService().json_parse(
#             communicationService.CommunicationService().parseheaders(request)['TESTINFORMATION'])
#         print test["TASKS"][1]
#         return Response(test)
#
#
# class AddObject(APIView):
#     def get(self, request):
#         pass
#
#     def post(self, request):
#         """
#         Used to add new test or category to the database.
#         :param request:
#         :return:
#         """
#         database = databaseService.DatabaseService()
#         database.add(request)
#         return Response(communicationService.CommunicationService().parseheaders(request))
#
#
# class Results(APIView):
#     def post(self, request):
#         """
#         Not used currently.
#         :param request:
#         :return:
#         """
#         return HttpResponse("hello")
