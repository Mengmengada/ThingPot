# from services import communicationService, attackService, databaseService
from django.http import HttpResponse
from rest_framework.views import APIView, Response
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        return Response({"success":{"username": "15A1OA1gfdeyUEvPNxa54pW1J07-yQEntEkPkEGd"}})


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
