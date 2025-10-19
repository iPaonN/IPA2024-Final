#######################################################################################
# Yourname: Panot Liangpiboon
# Your student ID: 66070112
# Your GitHub Repo: https://github.com/iPaonN/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.
import requests
import os
import restconf_final
from dotenv import load_dotenv
import time
import json

load_dotenv(override=True)
#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

print("Current working directory:", os.getcwd())
print("ACCESS_TOKEN value:", repr(ACCESS_TOKEN))

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (os.getenv("roomIdToGetMessages"))

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": "Bearer " + ACCESS_TOKEN}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    print("Response status code:", r.status_code)
    print("Response headers:", dict(r.headers))
    print("Response text:", r.text)
    
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}. Response: {}".format(r.status_code, r.text)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/" + "66070112" + " "):

        # extract the command
        command = message[len("66070112") + 2:]
        print(command)

# 5. Complete the logic for each command

        if command == "create":
            responseMessage = restconf_final.create()  
        elif command == "delete":
            responseMessage = restconf_final.delete()
        elif command == "enable":
            responseMessage = restconf_final.enable()
        elif command == "disable":
            responseMessage = restconf_final.disable()
        # elif command == "status":
        #     <!!!REPLACEME with code for status command!!!>
        #  elif command == "gigabit_status":
        #     <!!!REPLACEME with code for gigabit_status command!!!>
        # elif command == "showrun":
        #     <!!!REPLACEME with code for showrun command!!!>
        else:
            responseMessage = "Error: No command or unknown command"
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            # filename = "<!!!REPLACEME with show run filename and path!!!>"
            # fileobject = <!!!REPLACEME with open file!!!>
            # filetype = "<!!!REPLACEME with Content-type of the file!!!>"
            # postData = {
            #     "roomId": <!!!REPLACEME!!!>,
            #     "text": "show running config",
            #     "files": (<!!!REPLACEME!!!>, <!!!REPLACEME!!!>, <!!!REPLACEME!!!>),
            # }
            # postData = MultipartEncoder(<!!!REPLACEME!!!>)
            # HTTPHeaders = {
            # "Authorization": ACCESS_TOKEN,
            # "Content-Type": <!!!REPLACEME with postData Content-Type!!!>,
            # }
            continue # don't forget to remove
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": os.getenv("roomIdToGetMessages"), "text": responseMessage}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {
                "Authorization": "Bearer " + ACCESS_TOKEN,
                "Content-Type": "application/json"
            }

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
