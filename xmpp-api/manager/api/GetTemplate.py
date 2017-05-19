import json
import logging

import Service


def get_complete_template():
    """
    DIRTY
    :return: Dictionary why
    """
    with open('api/template.json') as data:
        a = data.read()
    b = json.loads(a)
    return b

# def get_complete_template():
#     with open('api/template.json') as data:
#         d = json.loads(data.read())
#         r = json.dumps(        )
#     return d

def set_light(light_id, request):
    # prequest.body
    body_dic = json.loads(request.body)
    key_list = []
    for key in body_dic.keys():
        key_list.append({"success":{"/lights/"+str(light_id)+"/"+ key:body_dic[key]}})
    print key_list
    # r = [{"success": key_list}]
    # d= [
    #     {
    #         "success": {
    #             "/lights/2/state/alert": "select"
    #         }
    #     }
    # ]
    return key_list


def get_light(light_id, request):
    with open('api/template.json') as data:
        d = json.loads(data.read())
    if light_id:
        r = d["lights"][str(light_id)]
    else:
        r=d["lights"]
    return r

def get_config(request):
    with open('api/template.json') as data:
        d = json.loads(data.read())
    r=d["config"]
    return r

def set_config(request):
    body_dic = json.loads(request.body)
    key_list = []
    for key in body_dic.keys():
        key_list.append({"success":{"/config/"+"/"+ key:body_dic[key]}})
    print key_list
    # r = [{"success": key_list}]
    # d= [
    #     {
    #         "success": {
    #             "/lights/2/state/alert": "select"
    #         }
    #     }
    # ]
    return key_list

def err_msg(request):
    usrname = Service.gen_rand_str()
    r=[{"error": {"type": 3,"address": "/config/" + usrname,"description": "resource, /config/dfdf, not available"}}]
    print r
    return r