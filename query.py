from vmanage_api import rest_api_lib
from settings import *
from urllib.parse import quote
import json

uuid = "b28d5637-d966-4898-a103-7e7e8d595b50"
hostname = "Training-LAS-1"

vm_session = rest_api_lib(vmanage_add, vmanage_user, vmanage_password)
query = {
    "size": 100,
    "query": {
        "condition": "OR",
        "rules": [{
            "value": [uuid],
            "field": "uuid",
            "type":"string",
            "operator": "in"
        }
        ]
    }
}

# query = {
#   "size": 100,
#   "query": {
#     "condition": "AND",
#     "rules": [
#       {
#         "value": [
#           "100"
#         ],
#         "field": "vpn_id",
#         "type": "int",
#         "operator": "equal"
#       }
#     ]
#   }
# }

url = '/alarms'
url += f'?query={quote(json.dumps(query))}'
response = vm_session.get_request(url)
vm_session.logout()
print(response)
if response['data'] is []:
    print('no data')
else:
    for x in response['data']:
        print(x['component'])
