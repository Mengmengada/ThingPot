
def Replyaccept_event_req(self, iq, request_delay_sec, seqnr):
    iq.reply();  # Here the iq changed(before is the received, now is a new one with type 'result')
    iq['accepted']['seqnr'] = seqnr;
    if not request_delay_sec is None:
        iq['accepted']['queued'] = "true"
    return iq

def Replymessage_event_req(self,session, nodes, fields):
    msg = self.xmpp.Message();
    msg['from'] = self.sessions[session]['to'];
    msg['to'] = self.sessions[session]['from'];
    msg['fields']['seqnr'] = self.sessions[session]['seqnr'];
    nodes['device'].refresh(fields)

    # if timestamp_block is not None and len(timestamp_block) > 0:
    #     node = msg['fields'].add_node(nodeId);
    #     ts = node.add_timestamp(timestamp_block["timestamp"]);
    #
    #     for f in timestamp_block["fields"]:
    #         data = ts.add_data(typename=f['type'],
    #                            name=f['name'],
    #                            value=f['value'],
    #                            unit=f['unit'],
    #                            dataType=f['dataType'],
    #                            flags=f['flags']);
    #
    #
    #     # self.sessions[session]["commTimers"][nodeId].cancel();
    # self.sessions[session]["nodeDone"][nodeId] = True;
    # msg['fields']['done'] = 'true';
    # if (self._all_nodes_done(session)):
    #     # The session is complete, delete it
    #     # print("del session " + session + " due to complete")
    #     del self.sessions[session];

    # msg = < message
    # to = "meng2@xmpp.jp/7219466258101789481491294806663733"
    # from="meng1@xmpp.jp/temperature"
    # xml:lang = "en" > < fields
    # xmlns = "urn:xmpp:iot:sensordata"
    # done = "true"
    # seqnr = "1" > < node
    # nodeId = "temperature" > < timestamp
    # value = "2017-04-04T10:32:06" > < numeric
    # value = "1000"
    # momentary = "true"
    # name = "Temperature"
    # unit = "C"
    # automaticReadout = "true" / > < / timestamp > < / node > < / fields > < / message >

    # msg.send();  # Here the message is sent out
    return msg
