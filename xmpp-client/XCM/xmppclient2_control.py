########################################################################################################################
#To control the philips hue
#Author: Meng Wang
import sys
import logging
import getpass
from optparse import OptionParser
from sleekxmpp.exceptions import IqError, IqTimeout
import sleekxmpp
from sleekxmpp import ClientXMPP

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')



class IoT_Client(sleekxmpp.ClientXMPP):
    """
    A simple IoT device that can act as client

    This script can act as a "client" an IoT device or other party that would like to get data from
    another device.

    Setup the command line arguments.

    python xmpp_client.py -j "bob@yourdomain.com" -p "password" -c "alice@yourdomain.com/device1" {--[debug|quiet]}
    python xmpp_client.py -j "bob@127.0.0.1" -p "password" -c "alice@127.0.0.1/device1" {--[debug|quiet]}
"""

    def __init__(self, jid, password, sensorjid):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.device = None
        self.releaseMe = False
        self.target_jid = sensorjid

    def datacallback(self, from_jid, result, nodeId=None, timestamp=None, fields=None,
                     error_msg=None):
        """
        This method will be called when you ask another IoT device for data with the xep_0323
        se script below for the registration of the callback
        """
        print  result, from_jid
        print "successful"
        self.disconnect()

    def testForRelease(self):
        # todo thread safe
        return self.releaseMe

    def doReleaseMe(self):
        # todo thread safe
        self.releaseMe = True

    def addDevice(self, device):
        self.device = device

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        # tell your preffered friend that you are alive using generic xmpp chat protocol
        # self.send_message(mto='jocke@jabber.sust.se', mbody=self.boundjid.bare +' is now online use xep_323 stanza to talk to me')

        # -------------------------------------------------------------------------------------------
        #   Service Discovery
        # -------------------------------------------------------------------------------------------
        try:
            # By using block=True, the result stanza will be
            # returned. Execution will block until the reply is
            # received. Non-blocking options would be to listen
            # for the disco_info event, or passing a handler
            # function using the callback parameter.
            #here get iq
            info = self['xep_0030'].get_info(jid=self.target_jid,
                                             node=None,
                                             block=True)
        except IqError as e:
            logging.error("Entity returned an error: %s" % e.iq['error']['condition'])
        except IqTimeout:
            logging.error("No response received.")
        else:
            header = 'XMPP Service Discovery'
            # print('-' * PRINT_HEADER_LENGTH)
            #gap = ' ' * ((PRINT_HEADER_LENGTH - len(header)) / 2)
            # print(gap + header)
            # print('-' * PRINT_HEADER_LENGTH)

            print "Device: %s" % self.target_jid
            #analysis the features of the target device
            for feature in info['disco_info']['features']:
                print('  - %s' % feature)

        # -------------------------------------------------------------------------------------------
        #   Requesting data through XEP0323
        # -------------------------------------------------------------------------------------------
        #Here!!!!!!!!!!!!!!!!!!!!!!
        # session = self['xep_0323'].request_data(self.boundjid.full, self.target_jid,
        #                                         self.datacallback, flags={"momentary": "true"})
        fields = (["on", "boolean", 0],["bri", "int", 254])
        # fields = (["on", "boolean", 1], ["toggle", "boolean", 1])
        # fields = (["bri", "numeric", 120], ["bri", "numeric", 12])
        session = self['xep_0325'].set_request(self.boundjid.full, self.target_jid, self.datacallback, fields )

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            logging.debug("got normal chat message" + str(msg))
            ip = socket.gethostbyname(socket.gethostname())
            msg.reply(
                "Hi I am " + self.boundjid.full + " and I am on IP " + ip + " use xep_323 stanza to talk to me").send()
        else:
            logging.debug("got unknown message type %s", str(msg['type']))


if __name__ == '__main__':
    # -------------------------------------------------------------------------------------------
    #   Parsing Arguments
    # -------------------------------------------------------------------------------------------
    optp = OptionParser()
    optp.add_option("-o", "--on", dest="on",
                    help="JID to use")
    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    # IoT sensor jid
    optp.add_option("-c", "--sensorjid", dest="sensorjid",
                    help="Another device to call for data on", default=None)


    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None or opts.password is None or opts.sensorjid is None:
        optp.print_help()
        exit()
    # -------------------------------------------------------------------------------------------
    #   Starting XMPP with XEP0030, XEP0323, XEP0325
    # -------------------------------------------------------------------------------------------
    xmpp = IoT_Client(opts.jid, opts.password, opts.sensorjid)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0323')
    xmpp.register_plugin('xep_0325')
    if opts.sensorjid:
        logging.debug("will try to call another device for data")
        xmpp.connect()
        print "connnnnnnn+++++++++++++++++++cted test!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        xmpp.process()
        logging.debug("ready ending")

    else:
        print "noopp didn't happen"