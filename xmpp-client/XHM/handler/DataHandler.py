import datetime
import yaml

def Datahandle_event_req(self, iq):
    # Assum the situation is that the iq get message is
    error_msg = '';  # accepted iq sent aftet this --commented by Meng
    req_ok = True;
    process_nodes = [];
    process_fields = [];
    request_delay_sec = None
    req_flags = iq['req']._get_flags();# ??? what is flags?
    DATA_FILE = "../XHC/xclient1.yaml"
    data = yaml.load(open(DATA_FILE))
    honeypot_mode = data['honeypot_mode']
    # Authentication IMPORTANT!!!!!!!!!!!!!!!!!!!!!!     --commented by Meng
    ##########################################################################
    # If we set req_ok always true, we can pass the authentication
    ##############################################################################
    if honeypot_mode:
        # honeypot mode, reply as a honeypot
        #when the honeypot_mode is true, the parameter to return will be hard coded. Here is for the logging part. to
        # take notes of the error from the attacker's message.
        # TODO: change the error_msg value to a particular kind of log
        req_ok = True;
        process_nodes = self.nodes.keys();
        process_fields = [];
        request_delay_sec = None
        req_flags = iq['req']._get_flags();
        if len(self.test_authenticated_from) > 0 and not iq['from'] == self.test_authenticated_from: # ??????
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
                    error_msg = "Invalid datetime in 'when' flag, cannot set a time in the past. Current time: " + dtnow.isoformat();

    else:
        #normal mode as a normal client
        if len(self.test_authenticated_from) > 0 and not iq['from'] == self.test_authenticated_from: # ??????
            # Invalid authentication
            req_ok = False;
            error_msg = "Access denied";

        # Nodes
        if len(iq['req']['nodes']) > 0:
            for n in iq['req']['nodes']:
                if not n['nodeId'] in self.nodes:
                    req_ok = False;
                    error_msg = "Invalid nodeId " + n['nodeId'];
            process_nodes = [n['nodeId'] for n in iq['req']['nodes']];
        else:
            process_nodes = self.nodes.keys();  # here give the process_nodes = temperature
        # Fields - if we just find one we are happy, otherwise we reject

        if len(iq['req']['fields']) > 0:
            found = False
            for f in iq['req']['fields']:
                for node in self.nodes:
                    if self.nodes[node]["device"].has_field(f['name']):
                        found = True;
                        break;
            if not found:
                req_ok = False;
                error_msg = "Invalid field " + f['name'];
            process_fields = [f['name'] for n in iq['req']['fields']];

        if 'when' in req_flags:
            # Timed request - requires datetime string in iso format
            # ex. 2013-04-05T15:00:03
            dt = None
            try:
                dt = datetime.datetime.strptime(req_flags['when'], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                req_ok = False;
                error_msg = "Invalid datetime in 'when' flag, please use ISO format (i.e. 2013-04-05T15:00:03)."

            if not dt is None:
                # Datetime properly formatted
                dtnow = datetime.datetime.now()
                dtdiff = dt - dtnow
                request_delay_sec = dtdiff.seconds + dtdiff.days * 24 * 3600
                if request_delay_sec <= 0:
                    req_ok = False;
                    error_msg = "Invalid datetime in 'when' flag, cannot set a time in the past. Current time: " + dtnow.isoformat();
    return error_msg, req_ok, req_flags, request_delay_sec, process_fields,process_nodes