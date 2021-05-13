# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:46:33 2021

@author: ruanr
"""

import time
import requests
import json


def sendToZenvia(messages,fromNumber="", toNumber=""):

    url = "https://api.zenvia.com/v2/channels/whatsapp/messages"
    for message in messages:

# =============================================================================
#         delay = len(message["text"])*10
#
#
#         if("[DELAY]" in message["text"]):
#             delay = 2000
#             message.text = message.text.replace("[DELAY]","")
#
#         time.sleep(delay/1000)
# =============================================================================

        if("[DOCUMENTO]" in message["text"]):
            payload = json.dumps({
            "from": fromNumber,
            "to": toNumber,
            "contents": [
              {
                "type": "file",
                "fileUrl": "https://images.template.net/wp-content/uploads/2015/12/29130015/Sample-Contract-Agreement-Template-PDF.pdf",
                "fileMimeType":"application/pdf",#document #application
                "fileCaption": "Documento de Proposta - Caption",
                "fileName":"Documento de Proposta"
              }
            ]
          })
        else:
          payload = json.dumps({
            "from": fromNumber,
            "to": toNumber,
            "contents": [
              {
                "type": "text",
                "text": message["text"]
              }
            ]
          })
        headers = {
          'X-API-TOKEN': 'WidvuSSb_qOm0fVJAEWn_pXCTzVAytY_uenE',
          'Content-Type': 'application/json'
        }
        try:
            requests.request("POST", url, headers=headers, data=payload)
        except:
            return False





if __name__ == "__main__":
    print(sendToZenvia([{"text":"teste"}],fromNumber="555131037415", toNumber="5511992448799"))