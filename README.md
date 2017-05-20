# XMPP IoT Honeypot

# Summary
IoT honeypot implementation of XMPP protocol. It includes two main modules: `Client` and `Server`

## Server Honeypot
To be added
## Client Honeypot
To be added

# Description
To be added


# Setup
This is an intruction for the phue branch, which has acheived:
* Integration of XMPP and Philips Hue(Phue). Thus Phue can be controlled through XMPP message or iq request.

* Simulation of Bridge's API. Thus to get simulated information of the Phue Bridge and Phue light through a valid HTTP request.
## Installation

The file dependencies.txt shows all the dependencies. You can easily install them by `pip install -r dependencies.txt`

### Integration of XMPP & Real Phue
The scripts is located on `xmpp-client/XCM/IoT_PhilipsHueApi_meng.py`.
This script will connect to the real bridge but not the REST API.
To run it you need the to configure some parameters:

-j `JID` -n `resource` -p `password` --individual `light_id` --bridgeip `IP_of_bridge` -d

e.g.: `-j meng1@xmpp.jp -n "light1" -p xmpptest -d --individual 1 --bridgeip 172.10.1.11`

See the instruction on: http://www.xmpp-iot.org/tutorials/python-philiphshue/

The bridgeip is optional

### Phue Bridge Api Simulation:
#### Running REST API

The running file is located at `xmpp-api/manager/manage.py`

command is:

`python manage.py runserver 127.0.0.1:3000`

the ip address and the port number can be changed.

#### Integration the simulated api and XMPP

The scripts is located on `xmpp-client/XCM/IoT_PhilipsHueApi_meng_api.py`.

The input parameters are almost the same but the `bridgeip` and the `apiport` is the ip and port that the rest api is running on

e.g. `-j meng1@xmpp.jp -n "light2" -p xmpptest -d --individual 1 --bridgeip 127.0.0.1 --apiport 3000`

#### Automatically subscribe a large number of Jabber ID(JID) on different xmpp servers

`IoT_PhilipsHueApi_meng_api.py` can only subscribe for one JID, which means one light at one time. While it will be more
efficient to run more JID.

`XMM/scan.py` can make much more JIDs listening on different servers by one command. It will read a configuration file
located at `xmpp-client/XHC/phuehoneypot_config.yaml`. And it can start threads for each of a JID

#### Interaction with the honeypot
The attacker or tester can reach and communicate with the honeypot in three ways:
* Sending HTTP request to where the REST API is running on.
* Sending an iq set stanza:
   `xmpp-client/XCM/xmppclient2_control.py` can send an iq set to "control the light".
   command is:
   -j `JID` -p `password` -c `TARGET_JID` -d
   command example: `-j meng1@jabber.at -p xmpptest -c meng1@xmpp.jp/light1 -d`
    Here the `TARGET_JID` is the JID that is listening on the server you set on the former step.

    For the content of the control you need to go into the code, in the functon `session_start` a variable called fields.
    e.g.: `fields=(["on", "boolean", 1],["bri", "int", 254])`
* Sending a iq get stanza
    `xmpp-client/thridparty/examples/xmppclient1.py` can send an iq get to get the information of the light that is registered.
    The command is the same ad "sending an iq set stanza"
* Sending an xmpp message
    By sending an xmpp message you can "control the light". You can achieve this by logging in any xmpp client, adding the
  JID that is listening on the server that you subscribed according to the former step (e.g. meng1@xmpp.jp/light2). Then
  send valid command. The valid command list is in `xmpp-client/XCM/IoT_PhilipsHueApi_meng_api.py` line around 303 with
  the variable `command`. It's basically command like on, off, bri=254, etc.

## Configuration
To be added

## Usage
To be added

## Examples
To be added

# Authors
To be added

# ToDo
To be added

# Changelog
To be added
