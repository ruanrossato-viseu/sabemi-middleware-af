# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 14:53:19 2021

@author: ruanr
"""

import requests
import json

baseUrl = "http://localhost:3000"

def sendToBotkit(message = "",userId=""):

    url = baseUrl +"/api/messages"

    payload = json.dumps({
      "type": "message",
      "text": message,
      "channel": "websocket",
      "user": userId
    })
    headers = {
      'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    print(sendToBotkit("Ola",123))