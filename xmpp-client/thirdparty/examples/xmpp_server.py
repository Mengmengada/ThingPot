#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
from optparse import OptionParser
import socket

import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding

    setdefaultencoding('utf8')
else:
    raw_input = input

from sleekxmpp.plugins.xep_0323.device import Device


class IoT_Server(sleekxmpp.ClientXMPP):
    """
    A simple IoT device that can act as server.

    This script can act as a "server" an IoT device that can provide sensor information.

    Setup the command line arguments.

    python xmpp_client.py -j "alice@yourdomain.com" -p "password" -n "device1" {--[debug|quiet]}
    python xmpp_client.py -j "alice@127.0.0.1" -p "password" -n "device1" {--[debug|quiet]}
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)#register,actually triggered here
        print "main function called????"
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
        print "++++++++++++++++++=session start==============="
        self.send_presence()
        self.get_roster()
        # tell your preffered friend that you are alive
        # self.send_message(mto='jocke@jabber.sust.se', mbody=self.boundjid.bare +' is now online use xep_323 stanza to talk to me')

    def message(self, msg):
        print "------------------------------------------------------------------------------message called"
        if msg['type'] in ('chat', 'normal'):
            logging.debug("got normal chat message" + str(msg))
            ip = socket.gethostbyname(socket.gethostname())
            msg.reply(
                "Hi I am " + self.boundjid.full + " and I am on IP " + ip + " use xep_323 stanza to talk to me").send()
        else:
            logging.debug("got unknown message type %s", str(msg['type']))

class IoT_Device(Device):
    """
    This is the actual device object that you will use to get information from your real hardware
    You will be called in the refresh method when someone is requesting information from you
    """

    def __init__(self, nodeId):
        Device.__init__(self, nodeId)
        print "device _init_ called +++++++++++++++++++++++"
        logging.debug("=========TheDevice.__init__ called==========")
        self.temperature = 25  # define default temperature value
        print self.temperature
        self.update_sensor_data()

    def refresh(self, fields):
        """
        the implementation of the refresh method
        """
        logging.debug("=========TheDevice.refresh called===========")
        print "device.refresh????????????????????????????????????????????/"
        self.temperature += 1  # increment default temperature value by one
        self.update_sensor_data()

    def update_sensor_data(self):
        logging.debug("=========TheDevice.update_sensor_data called===========")
        print "++++++++++++++++updat_sensor data!+++++++++++++"
        self._add_field(name="Temperature", typename="numeric", unit="C")
        self._set_momentary_timestamp(self._get_timestamp())
        self._add_field_momentary_data("Temperature", self.get_temperature(),
                                       flags={"automaticReadout": "true"})
        print "temperature::::::"+ self.get_temperature()

    def get_temperature(self):
        return str(self.temperature)


if __name__ == '__main__':
    # -------------------------------------------------------------------------------------------
    #   Parsing Arguments
    # -------------------------------------------------------------------------------------------
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    # IoT device id
    optp.add_option("-n", "--nodeid", dest="nodeid",
                    help="I am a device get ready to be called", default=None)

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None or opts.password is None or opts.nodeid is None:
        optp.print_help()
        exit()

    # -------------------------------------------------------------------------------------------
    #   Starting XMPP with XEP0030, XEP0323, XEP0325
    # -------------------------------------------------------------------------------------------

    # we bounded resource into node_id; because client can always call using static jid
    # opts.jid + "/" + opts.nodeid
    xmpp = IoT_Server(opts.jid + "/" + opts.nodeid, opts.password)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0323')
    xmpp.register_plugin('xep_0325')

    if opts.nodeid:
        myDevice = IoT_Device(opts.nodeid)
        print "++++nodeid++++"
        xmpp['xep_0323'].register_node(nodeId=opts.nodeid, device=myDevice, commTimeout=10)
        print "++++register completed_++++"
        while not (xmpp.testForRelease()):
            xmpp.connect()#to xmpp server,the session_start is called here
            xmpp.process(block=True)
            logging.debug("lost connection")