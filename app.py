# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:46:43 2021

@author: ruanr
"""

import flask
from flask import request
from botkit import sendToBotkit
from zenvia import sendToZenvia
# from mongo import getUserSession


app = flask.Flask(__name__)


@app.route('/message', methods=['POST'])
def incomingMessage():

    body = request.json
    userNumber = body["message"]["from"]
    botNumber = body["message"]["to"]
    message=""
    messageType = body["message"]["contents"][0]["type"]
    if(messageType=='text'):
        message = body["message"]["contents"][0]["text"]
    elif(messageType=='file'):
        message = body["message"]["contents"][0]["fileUrl"]


    replyFromBotkit = sendToBotkit(message,userNumber)

    replyFromZenvia = sendToZenvia(replyFromBotkit,botNumber, userNumber)
    return ""


if __name__ == "__main__":
    app.run()


# =============================================================================
#     {
#     "id": "191e19ab-b0b2-4baf-b48c-46e23da76a0c",
#     "timestamp": "2021-04-12T03:52:37.827Z",
#     "type": "MESSAGE",
#     "subscriptionId": "cf3e07b1-6892-42b0-98b2-53f68763ed2a",
#     "channel": "whatsapp",
#     "direction": "IN",
#     "message": {
#         "id": "4b1d75b6-93af-41f7-82a9-aa0ea91a4e0d",
#         "from": "5511992448799",
#         "to": "blush-country",
#         "direction": "IN",
#         "channel": "whatsapp",
#         "visitor": {
#             "name": "Ruan Rossato",
#             "firstName": "Ruan",
#             "lastName": "Rossato"
#         },
#         "contents": [
#             {
#                 "type": "text",
#                 "text": "asd"
#             }
#         ],
#         "timestamp": "2021-04-12T03:52:36+00:00"
#     }
# =============================================================================
