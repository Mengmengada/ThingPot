import yaml
import os
import threading
from datetime import datetime

<<<<<<< HEAD
DATA_FILE = "../XHC/phuehoneypot_config.yaml" # the configuration file, which includes the xmpp accounts infomation
data = yaml.load(open(DATA_FILE))
filename = "phue_api" #first part of the name of the log files
filepath = "../XLM/test" # path to where the log files will be saved
=======
DATA_FILE = "../XHC/phuehoneypot_config.yaml" # config file for the xmpp honeypot
data = yaml.load(open(DATA_FILE))
filepath = data['filepath'][0] # where all the log files will be stored, to modify in the config file
sysfilepath = filepath +"/" +"syslog"+datetime.now().strftime('%Y-%m-%d')  # the path of the system log file for each account
trafficfilename = filepath+"/"+"xmpplog"+datetime.now().strftime('%Y-%m-%d') +".log" # the name of the log file for all the traffic for all the accounts
>>>>>>> dev
list = []
apiusername = data["apiusername"][0] # username of the "bridge" that will be used when send api request, to modify in the config file
apiip = data["apiip"][0]
for name in data["names"]:
    # print values
    for domain in data["domains"]:
        for resource in data["resources"]:
            tup1 = (str(name), str(domain), str(resource))
            list.append(tup1)
<<<<<<< HEAD
# for tuple in list:
#     print tuple[0]
def xmengpp_client(barejid,nodeid,filename):
    os.system("python ../XCM/xmengpp_client.py -j"+ barejid+" -n"+nodeid+" -p xmpptest -d ")
def Phue_api(name, domain, resource,filename):
    var = "python ../XCM/IoT_PhilipsHueApi_meng_api.py -j " + name + "@" \
          + domain + " -n " + resource + \
          " -p xmpptest1218 -d --individual 1 --bridgeip 127.0.0.1 --apiport 3000 --logfile " + filename
    # print var
=======


def Phue_api(name, domain, resource, apiusername, sysfilename, trafficfilename):
    var = "python ../XCM/IoT_PhilipsHueApi_meng_api.py -j " + name + "@" + domain + " -n " + resource + \
          " -p xmpptest1218 -d --individual 1 --bridgeip "+apiip+" --apiport 3000 --apiusername " + \
          apiusername + " --syslogfile " + sysfilename +" --trafficlogfile " + trafficfilename
    print var
>>>>>>> dev
    os.system(var)


i = 0
os.system("mkdir " + sysfilepath) #make a directory for the system log file, will store the log file for each account
for tuple in list:
    # file=filename+str(i)+".log"
    sysfile = tuple[0] + "@" + tuple[1] + tuple[2] + ".log"
    task = threading.Thread(target=Phue_api, args=(tuple[0], tuple[1], tuple[2], apiusername, sysfilepath + "/" +
                                                   sysfile, trafficfilename))
    task.start()
    # i+=1

# task1 = threading.Thread(target=xmengpp_client, args=("meng1@jabber.at", "light", "1at_light.txt"))
# task2 = threading.Thread(target=xmengpp_client, args=("meng1@jabber.at", "temperature", "1at_temperature.txt"))
# task3 = threading.Thread(target=xmengpp_client, args=("meng2@xmpp.jp","light","2jp_light.txt"))
# task1.start()
# task2.start()
# task3.start()
