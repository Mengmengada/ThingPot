#Author: Meng Wang
#an xmpp client that supposed to have a sensor and provide data

from optparse import OptionParser
from thirdparty import sleekxmpp

from thirdparty.sleekxmpp.plugins.xep_0323.device import Device #plugin for iot xep
import logging
import socket
import yaml

class Client_SendTemp(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.device = None
        self.releaseMe = False

    def testForRelease(self):
        # todo thread safe
        return self.releaseMe

    def doReleaseMe(self):
        # todo thread safe
        self.releaseMe = True

    def addDevice(self, device):
        self.device = device

    def session_start(self, event):
        print "_____________________________session_start____________________"
        logging.debug("session start")
        self.send_presence()
        self.get_roster()
        # tell your preffered friend that you are alive
        # self.send_message(mto='jocke@jabber.sust.se', mbody=self.boundjid.bare +' is now online use xep_323 stanza to talk to me')

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            logging.debug("got normal chat message" + str(msg))
            ip = socket.gethostbyname(socket.gethostname())
            msg.reply(
                "Hi I am " + self.boundjid.full + " and I am on IP " + ip + " use xep_323 stanza to talk to me").send()
        else:
            logging.debug("got unknown message type %s", str(msg['type']))


class Device_TempSensor(Device):
    """
    This is the actual device object that you will use to get information from your real hardware
    You will be called in the refresh method when someone is requesting information from you
    """

    def __init__(self, nodeId):
        Device.__init__(self, nodeId)
        logging.debug("=========TheDevice.__init__ called==========")
        self.temperature = 1000# define default temperature value
        self.count = 1
        self.update_sensor_data()

    def refresh(self, fields):
        """
        the implementation of the refresh method
        """
        logging.debug("=========TheDevice.refresh called===========")
        print "someone is asking data , %s times", self.count
        logging.debug("information is asked for %s times", self.count
                      )

        self.count += 1  # increment default temperature value by one
        self.update_sensor_data()
        # self.update_sensor_data()

    # def update_sensor_data(self):
    #     logging.debug("=========TheDevice.update_sensor_data called===========")
    #     self._add_field(name="Temperature", typename="numeric", unit="C")
    #     self._set_momentary_timestamp(self._get_timestamp())
    #     self._add_field_momentary_data("Temperature", self.get_temperature(),
    #                                    flags={"automaticReadout": "true"})
    def update_sensor_data(self):
        logging.debug("=========TheDevice.update_sensor_data called===========")
        print "+++++++++++++++++++++update_sensor_data++++++++++++++++++++++++++++++++++"
        self._add_field(name="Temperature", typename="numeric", unit="C")
        self._set_momentary_timestamp(self._get_timestamp())
        self._add_field_momentary_data("Temperature", self.get_temperature(),
                                       flags={"automaticReadout": "true"})
        print "temperature::::::"+ self.get_temperature()
    def get_temperature(self):
        return str(self.temperature)



if __name__ == '__main__':


    optp = OptionParser()
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')
    #use the configuration file
    DATA_FILE = "../XHC/xclient1.yaml"
    data = yaml.load(open(DATA_FILE))
    jid = data['JID']['node'] + "@" + data['JID']['domain']
    nodeid = data['resource']
    password = data['password']
    # jidmeng1 = "meng1@xmpp.jp"
    # nodeid = "temperatu"
    # passwordmeng1 = "xmpptest"
    xmpp = Client_SendTemp(jid + "/" + nodeid, password)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0323')
    xmpp.register_plugin('xep_0325')

    if nodeid:
        myDevice = Device_TempSensor(nodeid)
        xmpp['xep_0323'].register_node(nodeId=nodeid, device=myDevice, commTimeout=10)
        while not (xmpp.testForRelease()):
            xmpp.connect()  # to xmpp server,the session_start is called here
            # print "the IP address is : " #+ xmlstream.XMLStream.pick_dns_answer(BaseXMPP.jid.,5222)
            xmpp.process(block=True)
            logging.debug("lost connection")