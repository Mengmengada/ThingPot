import yaml
import os
import threading

DATA_FILE = "../XHC/phuehoneypot_config.yaml"
data = yaml.load(open(DATA_FILE))
filename = "phue_api"
filepath = "../XLM/test"
list = []
for name in data["names"]:
    # print values
    for domain in data["domains"]:
        for resource in data["resources"]:
            tup1 = (str(name), str(domain), str(resource))
            list.append(tup1)
# for tuple in list:
#     print tuple[0]
def xmengpp_client(barejid,nodeid,filename):
    os.system("python ../XCM/xmengpp_client.py -j"+ barejid+" -n"+nodeid+" -p xmpptest -d ")
def Phue_api(name, domain, resource,filename):
    var = "python ../XCM/IoT_PhilipsHueApi_meng_api.py -j " + name + "@" + domain + " -n " + resource + " -p xmpptest1218 -d --individual 1 --bridgeip 127.0.0.1 --apiport 3000 --logfile " + filename
    # print var
    os.system(var)
i=0
os.system("mkdir "+filepath)
for tuple in list:
    # file=filename+str(i)+".log"
    print tuple
    file = tuple[0]+"@"+tuple[1]+tuple[2]+".log"
    task = threading.Thread(target=Phue_api, args=(tuple[0], tuple[1], tuple[2], filepath+"/"+file))
    task.start()
    # i+=1

# task1 = threading.Thread(target=xmengpp_client, args=("meng1@jabber.at", "light", "1at_light.txt"))
# task2 = threading.Thread(target=xmengpp_client, args=("meng1@jabber.at", "temperature", "1at_temperature.txt"))
# task3 = threading.Thread(target=xmengpp_client, args=("meng2@xmpp.jp","light","2jp_light.txt"))
# task1.start()
# task2.start()
# task3.start()