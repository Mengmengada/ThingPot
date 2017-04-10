import yaml

DATA_FILE = "../XHC/scan_config.yaml"
data = yaml.load(open(DATA_FILE))

# for name in data:
#     for values in data[name]:
#         print values

list = []
for values in data["names"]:
    # print values
    for d in data["domains"]:
        for r in data["resources"]:
            tup1 = (values, d, r)
            list.append(tup1)
for tuple in list:
    print tuple

