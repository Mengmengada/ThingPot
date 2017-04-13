# import yaml
import os
import threading

# DATA_FILE = "../XHC/scan_config.yaml"
# data = yaml.load(open(DATA_FILE))
#
# list = []
# for values in data["names"]:
#     # print values
#     for d in data["domains"]:
#         for r in data["resources"]:
#             tup1 = (values, d, r)
#             list.append(tup1)
# for tuple in list:
#     print tuple
def xmengpp_client(barejid,nodeid,filename):
    os.system("python ../XCM/xmengpp_client.py -j"+ barejid+" -n"+nodeid+" -p xmpptest -d >>"+filename)

task1 = threading.Thread(target=xmengpp_client, args=("meng1@jabber.at", "light", "1at_light.txt"))
task2 = threading.Thread(target=xmengpp_client, args=("meng1@jabber.at", "temperature", "1at_temperature.txt"))
task3 = threading.Thread(target=xmengpp_client, args=("meng2@xmpp.jp","light","2jp_light.txt"))
task1.start()
task2.start()
task3.start()