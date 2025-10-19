import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

requests.packages.urllib3.disable_warnings()

api_url = os.getenv("API_URL")

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = (os.getenv("userNAME"), os.getenv("passWORD"))

def debug_env():
    print("=== Environment Debug ===")
    print(f"API_URL: {os.getenv('API_URL')}")
    print(f"USERNAME: {os.getenv('userNAME')}")
    print(f"PASSWORD: {os.getenv('passWORD')}")
    print(f"Basic Auth Tuple: {(os.getenv('userNAME'), '*' * len(os.getenv('passWORD', '')) if os.getenv('passWORD') else 'None')}")
    print("========================")


def create():
    debug_env()
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070112",
            "description": "Created via RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.1.12.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }

    resp = requests.post(
        api_url + "data/ietf-interfaces:interfaces",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface 66070112 created successfully."
    elif resp.status_code == 409:
        print('Cannot create: Interface loopback 66070112 {}'.format(resp.text))
        return "Cannot create: Interface loopback 66070112: Interface 66070112 already exists."
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Create failed."


# def delete():
#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))


# def enable():
#     yangConfig = <!!!REPLACEME with YANG data!!!>

#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         data=json.dumps(<!!!REPLACEME with yangConfig!!!>), 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))


# def disable():
#     yangConfig = <!!!REPLACEME with YANG data!!!>

#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         data=json.dumps(<!!!REPLACEME with yangConfig!!!>), 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))


# def status():
#     api_url_status = "<!!!REPLACEME with URL of RESTCONF Operational API!!!>"

#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         response_json = resp.json()
#         admin_status = <!!!REPLACEME!!!>
#         oper_status = <!!!REPLACEME!!!>
#         if admin_status == 'up' and oper_status == 'up':
#             return "<!!!REPLACEME with proper message!!!>"
#         elif admin_status == 'down' and oper_status == 'down':
#             return "<!!!REPLACEME with proper message!!!>"
#     elif(resp.status_code == 404):
#         print("STATUS NOT FOUND: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))
