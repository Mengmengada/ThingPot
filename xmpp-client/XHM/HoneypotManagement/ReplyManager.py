

def ReplyManage_event_req(self, iq, req_ok, request_delay_sec, seqnr, error_msg):
    if req_ok:
        iq.reply();  # Here the iq changed(before is the received, now is a new one with type 'result')
        iq['accepted']['seqnr'] = seqnr;
        if not request_delay_sec is None:
            iq['accepted']['queued'] = "true"
    else:
        iq.reply();
        iq['type'] = 'error';
        iq['rejected']['seqnr'] = seqnr;
        iq['rejected']['error'] = error_msg;
    return iq
