import json
import logging

import Service


def get_complete_template():
    """
    DIRTY
    :return: Dictionary why
    """
    # with open('api/template.json') as data:
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
        key_list.append({"success": {"/lights/" + str(light_id) + "/" + key: body_dic[key]}})
    # print key_list
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
        r = d["lights"]
    return r


def get_config(request):
    with open('api/template.json') as data:
        d = json.loads(data.read())
    r = d["config"]
    return r


def get_whatever(request, _key):
    key = str(_key)
    with open('api/template.json') as data:
        d = json.loads(data.read())
    flag = False
    for x in d:
        if str(key) == x:
            r = d[key]
            flag = True
    if flag == False:
        r = error(4, key)
    # r=d["config"]
    return r


def set_config(request,_key):
    body_dic = json.loads(request.body)
    key_list = []
    for key in body_dic.keys():
        key_list.append({"success": {_key + "/" + key: body_dic[key]}})
    return key_list


def err_msg(request):
    usrname = Service.gen_rand_str()
    r = [{"error": {"type": 3, "address": "/config/whitelist/" + usrname,
                    "description": "resource, /config/whitelist/" + usrname + ", not available"}}]
    print r
    return r


def error(type_id, req):
    address = "/" + req
    err = [{"error": {"type": type_id, "address": address,
                      "description": "method, GET, not available for resource, " + address}}]
    return err
