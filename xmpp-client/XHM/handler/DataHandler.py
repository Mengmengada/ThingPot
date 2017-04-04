import datetime
from threading import Thread, Lock, Timer
import yaml
from XHM.HoneypotManagement import ReplyManager
import logging
####To handle the iq message from others that is requesting device data

def Datahandle_handle_event_req(self, iq, seqnr, session):
    # Assum the situation is that the iq get message is
    error_msg = '';  # accepted iq sent aftet this --commented by Meng
    ##########################################################################
    # If we set req_ok always true, we can pass the authentication
    ##############################################################################
    # honeypot mode, reply as a honeypot
    # when the honeypot_mode is true, the parameter to return will be hard coded. Here is for the logging part. to
    # take notes of the error from the attacker's message.
    # TODO: change the error_msg value to a particular kind of log
    logging.debug("___Datahandle_handle_event_req is called___")
    req_ok = True;
    process_nodes = self.nodes.keys();
    process_fields = [];
    request_delay_sec = None
    req_flags = iq['req']._get_flags();
    ####################################################
    #For logging
    #######################################################
    if len(self.test_authenticated_from) > 0 and not iq['from'] == self.test_authenticated_from:  # ??????
        # Invalid authentication
        error_msg = "Access denied";
    # Nodes
    if len(iq['req']['nodes']) > 0:
        for n in iq['req']['nodes']:
            if not n['nodeId'] in self.nodes:
                error_msg = "Invalid nodeId " + n['nodeId'];
    # Fields - if we just find one we are happy, otherwise we reject
    if len(iq['req']['fields']) > 0:
        found = False
        for f in iq['req']['fields']:
            for node in self.nodes:
                if self.nodes[node]["device"].has_field(f['name']):
                    found = True;
                    break;
        if not found:
            error_msg = "Invalid field " + f['name'];
        process_fields = [f['name'] for n in iq['req']['fields']];
    if 'when' in req_flags:
        # Timed request - requires datetime string in iso format
        # ex. 2013-04-05T15:00:03
        dt = None
        try:
            dt = datetime.datetime.strptime(req_flags['when'], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            error_msg = "Invalid datetime in 'when' flag, please use ISO format (i.e. 2013-04-05T15:00:03)."

        if not dt is None:
            # Datetime properly formatted
            dtnow = datetime.datetime.now()
            dtdiff = dt - dtnow
            request_delay_sec = dtdiff.seconds + dtdiff.days * 24 * 3600
            if request_delay_sec <= 0:
                error_msg = "Invalid datetime in 'when' flag, cannot set a time in the past. Current time: "\
                            + dtnow.isoformat();
    #Make a new session to send the accepted iq back
    # session = self._new_session();
    # self.sessions[session] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr};
    # self.sessions[session]["commTimers"] = {};
    # self.sessions[session]["nodeDone"] = {};
    # print("added session: " + str(self.sessions))

    iq_accept = ReplyManager.Replyaccept_event_req(self, iq, request_delay_sec, seqnr)
    iq_accept.send(block=False);  # Here the message is sent

    # Build the message that contains data:
    self.sessions[session]["node_list"] = process_nodes;
    # fields = self.nodes[node]['device'].fields.keys
    # msg_field = ReplyManager.Replymessage_event_req(self,session, self.nodes, fields)
    if not request_delay_sec is None:
        # Delay request to requested time
        timer = Timer(request_delay_sec, self._event_delayed_req, args=(session, process_fields, req_flags))
        self.sessions[session]["commTimers"]["delaytimer"] = timer;
        timer.start();
        return

    if self.threaded:
        tr_req = Thread(target=self._threaded_node_request,
                        args=(session, process_fields, req_flags))  # call the refresh function to get the data
        tr_req.start()
        print("started thread")
    else:
        ReplyManager.Replymessage_event_req(self, session, process_fields, req_flags, process_nodes);


    return iq_accept
