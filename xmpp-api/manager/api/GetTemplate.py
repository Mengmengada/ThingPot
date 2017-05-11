import json
import logging
def get_complete_template():
    with open('api/template.json') as data:
        d = json.loads(data.read())
    return d

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