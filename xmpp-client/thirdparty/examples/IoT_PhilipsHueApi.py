#!/usr/bin/env python

"""
    SleekXMPP: The Sleek XMPP Library
    Implementation of xeps for Internet of Things
    http://wiki.xmpp.org/web/Tech_pages/IoT_systems
    Copyright (C) 2013 Sustainable Innovation, Joachim.lindborg@sust.se
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""



import os
import sys
import socket
import json
from urllib import urlopen
from time import sleep

# This is based on the phue python hue bridge software
# clone the git clone https://github.com/studioimaginaire/phue.git at parallel directory to SleekXMPP
# or install in python
# This can be used when you are in a test environment and need to make paths right

#Basically this is to register the light on xmpp server and then we can get the information of these lights -Meng
sys.path=[os.path.join(os.path.dirname(__file__), '../..'),os.path.join(os.path.dirname(__file__), '../../../phue')]+sys.path

bridge=None

import logging
import unittest
import distutils.core
import datetime

from glob import glob
from os.path import splitext, basename, join as pjoin
from optparse import OptionParser
from urllib import urlopen

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
    
from sleekxmpp.plugins.xep_0323.device import Device as SensorDevice
from sleekxmpp.plugins.xep_0325.device import Device as ControlDevice
from phue import Bridge
class DummyBridge():
    def __init_(self):
        logging.warning("You are know using a dummy bridge")
    def set_light(self,dummy1,dummy2):
        logging.debug('dummybridge')
    def set_group(self,dummy1,dummy2):
        logging.debug('dummybridge')
    def get_light(self,dummy):
        logging.debug('dummybridge')
    def get_light(self,dummy):
        logging.debug('dummybridge')
        return {u'name': u'Attic hall', u'swversion': u'66010820', u'pointsymbol': {u'1': u'0f0000ffff00003333000033330000ffffffffff', u'3': u'none', u'2': u'none', u'5': u'none', u'4': u'none', u'7': u'none', u'6': u'none', u'8': u'none'}, u'state': {u'on': True, u'hue': 25400, u'colormode': u'hs', u'effect': u'none', u'alert': u'select', u'xy': [0.41110000000000002, 0.51649999999999996], u'reachable': True, u'bri': 254, u'sat': 254, u'ct': 293}, u'type': u'Extended color light', u'modelid': u'LCT001'}
    def get_group(self,dummy):
        logging.debug('dummybridge')
        return {u'action': {u'on': True, u'hue': 3000, u'colormode': u'xy', u'effect': u'none', u'xy': [0.64380000000000004, 0.34499999999999997], u'bri': 64, u'sat': 254, u'ct': 500}, u'lights': [u'1', u'2', u'3', u'4'], u'name': u'Lightset 0'}
                      
class BridgeContainer():
    
    def __init__(self,transitiontime=50,individual=None,ip=None,dummy=False):
        if dummy:
            self.mybridge=DummyBridge()
            self.individual=1
            self.transitiontime = 50
            return
        
        self.mybridge=None    
        while not self.mybridge:
            try:
                if not ip:
                    # try to find a bridge with meethue api
                    logging.debug("will try finding the hue bridge")
                    print "1111"
                    localbridge=json.loads(urlopen(' /nupnp').read())
                    ip=localbridge[0]["internalipaddress"]
                    logging.info('connecting to localbridge at '+str(ip))
                    print "????"
                self.mybridge=Bridge(ip)
                self.mybridge.connect()
                self.mybridge.get_api()
            except Exception as e:
                logging.warn('failed to connect to HUE server did you push the button?')
                self.mybridge=None    

            sleep(10)

        self.transitiontime = transitiontime
        self.individual = None
        if individual:
            self.individual=int(individual)
        self.alert()
        
    def setTransitionTime(self,value):
        # this should be the transistion time in seconds
        self.transitiontime = int(10 * float(value))

    def sendAll(self, **options):
        lamp = self.individual or 0
        for k,v in options.iteritems():
            if v is None:
                del(options[k])
        if self.transitiontime >= 0:
            options['transitiontime'] = self.transitiontime
        if self.individual:
            self.mybridge.set_light(self.individual, options)
        else:
            self.mybridge.set_group(0, options)

    def getAll(self):
        # returns dictionary with all values
        # {"state": {"on":true,"bri":254,"hue":45000,"sat":253,"xy":[0.1914,0.0879],"ct":500,"alert":"select","effect":"none","colormode":"hs","reachable":true},
        # "type": "Extended color light", "name": "Hue Lamp", "modelid": "LCT001", "swversion": "66009663", "pointsymbol": { "1":"none", "2":"none", "3":"none", "4":"none", "5":"none", "6":"none", "7":"none", "8":"none" }}
        return self.mybridge.get_light(self.individual)['state']

    def setEffect(self, value):
        self.sendAll(effect=effect)

    def setHue(self, value):
        self.sendAll(hue=value)

    def setBri(self, value):
        self.sendAll(bri=value)

    def setSat(self, value):
        self.sendAll(sat=value)

    def get_state(self):
        if self.individual:
            logging.debug(str(self.mybridge.get_light(self.individual)))
            return self.mybridge.get_light(self.individual)['state']

    def toggle(self, dummy=None):
        if self.individual:
            if self.mybridge.get_light(self.individual)['state']['on']:
                self.mybridge.set_light(self.individual, {'on': False})
            else:
                self.mybridge.set_light(self.individual, {'on': True})
        else:
            if self.mybridge.get_group(0)['action']['on']:
                self.mybridge.set_group(0, {'on': False})
            else:
                self.mybridge.set_group(0, {'on': True})

    def setOn(self, value):
        if self.individual:
            if value:
                self.mybridge.set_light(self.individual, {'on': True})
            else:
                self.mybridge.set_light(self.individual, {'on': False})

    def alert(self, dummy=None):
        if self.individual:
            self.mybridge.set_light(self.individual, {'alert':'select'})    
        else:
            self.mybridge.set_group(0, {'alert':'select'})    


#from sleekxmpp.exceptions import IqError, IqTimeout



class IoT_TestDevice(sleekxmpp.ClientXMPP):

    """
    A simple IoT device that can act as server or client both on xep 323 and 325
    """
    
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0323')
        self.register_plugin('xep_0325')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0199') # XMPP ping

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status",self.manage_status)

        #Some local status variables to use
        self.device=None
        self.beServer=True
        self.joinMucRoom=False
        self.clientJID=None
        self.controlJID=None
        self.received=set()
        self.controlField=None
        self.controlValue=None
        self.toggle=0
        self.room=""
        self.nick=""

    def datacallback(self,from_jid,result,nodeId=None,timestamp=None,fields=None,error_msg=None):
        """
        This method will be called when you ask another IoT device for data with the xep_0323
        se script below for the registration of the callback
        fields example
        [{'typename': 'numeric', 'unit': 'C', 'flags': {'momentary': 'true', 'automaticReadout': 'true'}, 'name': 'temperature', 'value': '13.5'},
        {'typename': 'numeric', 'unit': 'mb', 'flags': {'momentary': 'true', 'automaticReadout': 'true'}, 'name': 'barometer', 'value': '1015.0'},
        {'typename': 'numeric', 'unit': '%', 'flags': {'momentary': 'true', 'automaticReadout': 'true'}, 'name': 'humidity', 'value': '78.0'}]
        """
        
        if error_msg:
            logging.error('we got problem when recieving data %s', error_msg)
            return
        
        if result=='accepted':
            logging.debug("we got accepted from %s",from_jid)            
        elif result=='fields':
            logging.info("we got fields from %s with node %s",from_jid,nodeId)
            for field in fields:
                if field.has_key('unit'):
                    logging.info("Field %s %s %s",field['name'],field['value'],field['unit'])
                else:
                    logging.info("Field %s %s",field['name'],field['value'])
        elif result=='done':
            logging.debug("we got  done from %s",from_jid)

    def controlcallback(self,from_jid,result,error_msg,nodeIds=None,fields=None):
        """
        Called as respons to a xep_0325 control message 
        """
        logging.info('Control callback from %s result %s error %s',from_jid,result,error_msg)

    def getformcallback(self,from_jid,result,error_msg):    
        """
        called as respons to a xep_0325 get Form iq message
        """
        logging.debug("IoT got a form "+str(result))
        
    def addDevice(self, device):
        self.device=device

    def printRoster(self):
        logging.debug('Roster for %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            logging.debug('\n%s' % group)
            logging.debug('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    logging.debug(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    logging.debug(' %s [%s]' % (jid, sub))
                    
                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    logging.debug('   - %s (%s)' % (res, show))
                    if pres['status']:
                        logging.debug('       %s' % pres['status'])

    def manage_status(self, event):
        logging.debug("got a status update" + str(event.getFrom()))
        self.printRoster()
        
    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        # tell your preffered friend that you are alive 
        # self.send_message(mto='jabberjocke@jabber.se', mbody=self.boundjid.full +' is online use xep_323 to talk to me')
        self.send_message(mto='meng@xmpp.jp', mbody=self.boundjid.full +' is online +++++++++++++++++++++++++++++++')
        if self.joinMucRoom: #getting all the available node?   ---Meng
            logging.info("joining MUC room "+self.room+" as " +self.nick)
            self.plugin['xep_0045'].joinMUC(self.room,self.nick,wait=False)

    def help(self, dummy=None):
        status = bridge.get_state()
        reply=u"You had a question I cannot answer. Here's my status instead.\n"
        for key in ['on','bri','hue','sat','ct']:
            if status.has_key(key):
                reply+="\n"+key+"="+status[key]
        return reply

    def set_time(self, value):
        bridge.setTransitionTime(float(value))

    commands = {
        'on': lambda self, _: { 'on': True },
        'off': lambda self, _ : { 'on': False },
        'hue': lambda self, v: { 'hue': int(v) },
        'sat': lambda self, v: { 'sat': int(v) },
        'bri': lambda self, v: { 'bri': int(v) },
        'effect': lambda self, v: { 'effect': v },
        'fx': lambda self, v: { 'effect': v },
        'time': lambda self, v: self.set_time(v),
        'strawberry': lambda self, _: { 'hue': 0, 'sat': 255, 'bri': 255 },
        'fields': lambda self, _: None,
        'forever': lambda self, _: None,
        'orange': lambda self, _: { 'hue': 10000, 'sat': 255, 'bri': 192 },
        'a': lambda self, _: bridge.alert(),
        'alert': lambda self, _: bridge.alert(),
        'alarm': lambda self, _: bridge.alert(),
        'blink': lambda self, _: bridge.alert(),
        't': lambda self, _: bridge.toggle(),
        'toggle': lambda self, _: bridge.toggle(),
        'help': lambda self, _: self.help(),
        '_feck': lambda self, _: "Easy there, father Jack!",
    }

    def message(self, msg):
        if msg['type'] not in ('chat', 'normal','groupchat'):
            logging.debug("got unknown message type %s", str(msg['type']))
            return
        
        if msg['type']=='groupchat':
            if msg['mucnick'] == self.nick or self.nick in msg['body']:
                logging.debug("mirror message from room throw away")
                return
        #always reply to full JID
        replyto=msg['from'].full

        #parse the message
        cmd = msg['body'].lower().strip()
        
        if cmd.endswith('?'):
            #we send normal chat messages back
            self.send_message(mto=replyto, mbody=self.help())
            #msg.reply(self.help()).send()
            ##msg['type']='chat'
            return

        if cmd.startswith('hi'):
            internetip = urlopen('http://icanhazip.com').read()
            localip = socket.gethostbyname(socket.gethostname())
            jid=""
            if self.joinMucRoom:
                #we need to keep some privacy in the MUC rooms
                if msg['type']=='groupchat' or replyto.startswith(self.room) :
                    jid=self.nick
                else:
                    jid=self.boundjid.full
            else:
                jid=self.boundjid.full
            # self.send_message(mto=replyto, mbody=u" ".join((
            #     'I am',
            #     jid,
            #     'and I am on localIP',
            #     localip,
            #     'and on internet',
            #     internetip
            # )))
            return
        
        options = {}
        unknown = []
        for word in cmd.split():
            if '=' in word:
                word, value = word.split('=', 1)
            else:
                value = None

            if word.startswith('_'):
                word = word[1:]
            if word not in self.commands:
                unknown.append(word)
            else:
                res = self.commands[word](self, value)
                if isinstance(res, dict):
                    options.update(res)
                elif isinstance(res, (unicode, str)):
                    self.send_message(mto=replyto, mbody=res)

        if len(unknown) > 0:
            words = list((word for word in self.commands.keys() if word[0] != '_'))
            words.sort()
            if len(unknown) > 1:
                unknown = "%s, or %s" % (', '.join(unknown[:-1]), unknown[-1])
            else:
                unknown = unknown[0]
            self.send_message(mto=replyto, mbody="I have no idea why someone would use words like %s. I do love words like %s, and %s though." % (unknown, ", ".join(words[:-1]), words[-1]))

        if len(options) > 0:
            bridge.sendAll(**options)

            
class TheDevice(SensorDevice,ControlDevice):
    """
    Xep 323 SensorDevice
    This is the actual device object that you will use to get information from your real hardware
    You will be called in the refresh method when someone is requesting information from you

    xep 325 ControlDevice
    This 
    """
    def __init__(self,nodeId):
        SensorDevice.__init__(self,nodeId)
        ControlDevice.__init__(self,nodeId)
        self.counter=0
        self.relay=0


    def refresh(self,fields):
        """
        the implementation of the refresh method
        """
        status=bridge.get_state()

        self._set_momentary_timestamp(self._get_timestamp())
        # getvalues from lamps
        state=bridge.getAll()

        myDevice._add_field_momentary_data("transitiontime", str(bridge.transitiontime), flags={"automaticReadout": "true","momentary":"true","writable":"true"})
        # myDevice._add_field_momentary_data("hue", state['hue'], flags={"automaticReadout": "true","momentary":"true","writable":"true"})
        myDevice._add_field_momentary_data("on", state['on'], flags={"automaticReadout": "true","momentary":"true","writable":"true"})
        myDevice._add_field_momentary_data("toggle", False, flags={"automaticReadout": "true","momentary":"true","writable":"true"})
        myDevice._add_field_momentary_data("bri", state['bri'], flags={"automaticReadout": "true","momentary":"true","writable":"true"});
        # myDevice._add_field_momentary_data("sat", state['sat'], flags={"automaticReadout": "true","momentary":"true","writable":"true"});
        

    def _set_field_value(self, name,value):
        """ overrides the set field value from device to act on my local values                                            
        """
        logging.debug(" setting fields " + name + " to: " + str(value) )
        if name=="hue":
            bridge.setHue(int(value))
        elif name=="transitiontime":
            bridge.setTransitionTime(float(value))
        elif name=="bri":
            bridge.setBri(int(value))
        elif name=="sat":
            bridge.setSat(int(value))
        elif name=="toggle":
            bridge.toggle()
        elif name=="on":
            bridge.setOn(int(value))
        elif name=="alert":
            bridge.alert()
            
if __name__ == '__main__':

    # Setup the command line arguments.
    #
    # This script is an evolution from the IoT_TestDevice to integrate the web API from Philips HUE
    # Start this script in several instanses to control different lamps or the whole group
    # 
    #   Start with control of lamp individual 2
    #   python IoT_PhilipsHueApi.py -j "onelampJID@yourdomain.com" -p "password" -n "Lamp1" --individual 2 --bridgeip "192.168.2.22" --debug
    #
    #   starting without individual creates control of group 0
    #   python IoT_PhilipsHueApi.py -j "alllampsJID@yourdomain.com" -p "password" -n "LampGroup0" --bridgeip "192.168.2.22" --debug
    #
    #   If no bridgeip is provided 
    #   TODO: clean up inheritage from IoT_TestDevice
    
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    # IoT test
    optp.add_option("-n", "--nodeid", dest="nodeid",
                    help="Server (Provider) I am a device that can be called for data or send control to", default=None)
    optp.add_option("--individual", dest="individual",
                    help="setting the control to an individual", default=None)
    optp.add_option("--bridgeip", dest="bridgeip",
                    help="This is where the bridge is", default=None)
    optp.add_option("--room", dest="room",
                    help="MUC room to connect to", default=None)
    
    opts, args = optp.parse_args()

     # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    logging.debug("setting the individual to" + str(opts.individual))

    #connect to a bridge, use dummy true if you don't have a gateway nearby for testing 
    bridge=BridgeContainer(individual=opts.individual,ip=opts.bridgeip,dummy=False)
    
    #start up the XMPP client
    xmpp = IoT_TestDevice(opts.jid+ "/" + opts.nodeid,opts.password)
    # xmpp = IoT_TestDevice(opts.jid, opts.password)
    if opts.room:
        #we will be using a multiuser room chat to connect to
        #??????????????????
        xmpp.nick=opts.nodeid
        xmpp.room=opts.room
        xmpp.joinMucRoom=True
    
    
    # Instansiate the device object
    myDevice = TheDevice(opts.nodeid);
    myDevice._add_control_field(name="transitiontime", typename="numeric", value=50);
    myDevice._add_control_field(name="hue", typename="numeric", value=1);
    myDevice._add_control_field(name="on", typename="boolean", value=1);
    myDevice._add_control_field(name="toggle", typename="boolean", value=1);
    myDevice._add_control_field(name="bri", typename="numeric", value=1);
    myDevice._add_control_field(name="sat", typename="numeric", value=1);
    
    myDevice._add_field(name="transitiontime", typename="numeric", unit="ms")
    myDevice._add_field(name="hue", typename="numeric", unit="Count")
    myDevice._add_field(name="on", typename="boolean", unit="Count")
    myDevice._add_field(name="toggle", typename="boolean", unit="Count")
    myDevice._add_field(name="bri", typename="numeric", unit="Count")
    myDevice._add_field(name="sat", typename="numeric", unit="Count")
    
    myDevice._set_momentary_timestamp(myDevice._get_timestamp())
    myDevice._add_field_momentary_data("transitiontime", "0", flags={"automaticReadout": "true","momentary":"true","writable":"true"})
    myDevice._add_field_momentary_data("hue", "0", flags={"automaticReadout": "true","momentary":"true","writable":"true"})
    myDevice._add_field_momentary_data("on", "0", flags={"automaticReadout": "true","momentary":"true","writable":"true"})
    myDevice._add_field_momentary_data("toggle", "0", flags={"automaticReadout": "true","momentary":"true","writable":"true"})
    myDevice._add_field_momentary_data("bri", "0", flags={"automaticReadout": "true","momentary":"true","writable":"true"});
    myDevice._add_field_momentary_data("sat", "0", flags={"automaticReadout": "true","momentary":"true","writable":"true"});
    
    xmpp['xep_0323'].register_node(nodeId=opts.nodeid, device=myDevice, commTimeout=10);
    xmpp['xep_0325'].register_node(nodeId=opts.nodeid, device=myDevice, commTimeout=10);
    print "the nodeid is" + opts.nodeid
    
    xmpp.connect()
    xmpp.process(block=True)    
    logging.debug("lost connection")
