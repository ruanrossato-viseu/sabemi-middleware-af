# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 00:55:45 2021

@author: ruanr
"""


from pymongo import MongoClient

from datetime import datetime

# mongodb+srv://ruanrossato:<password>@sabemi.kvwlz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
client = MongoClient("mongodb+srv://ruanrossato:rmcr211096@sabemi.kvwlz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client["sabemi"]
currentUsers = database["currentUsers"]
interactions = database["interactions"]

def getUserSession(userId):
    user = currentUsers.find_one({"userId": userId})

    if(user):
        if((datetime.today()-user["lastInteraction"]).total_seconds() / 60.0 > 5):
            return createUserSession(userId)
        return user["sessionId"]
    else:
        return createUserSession(userId)


def createUserSession(userId):

    import sys

    user =  {
            "userId":userId,
            "lastInteraction":datetime.today().isoformat(),
            }

    try:
        result = currentUsers.insert_one(user)
        createInteraction(user["userId"],user["sessionId"])
        return(user["sessionId"])
    except:
        e = sys.exc_info()[0]
        print("Error", e)
        return False

def updateUserSession(sessionId):
    result = currentUsers.find_one_and_update(
        {"sessionId":sessionId},
        {"$set":{"lastInteraction":datetime.today()}}
    )

def createInteraction(userId,sessionId):
    interaction = {
                	"datetimeStart":datetime.today().isoformat(),
                	"datetimeFinish":"",
                	"user":{
                            "userId":userId,
                            },
                    "sessionId":sessionId,
                	"transfered":False,
                	"converted":False,
                	"events":[
                    		{
                 			"datetime":datetime.today().isoformat(),
                 			"type":"CreateIteraction",
                 			"agent":"middleware",
                 			}
                	]
                }

    result = interactions.insert_one(interaction)
    return result

def addMessageEvent(sessionId,incomingMessage,outgoingMessage):

    result = interactions.find_one_and_update(
        {"sessionId":sessionId},
        {"$push":{"events":{"$each":[
                {
                  "datetime":incomingMessage["date"],
                 	"type":"incomingMessage",
                 	"agent":"user",
                  "text":incomingMessage["text"],
                  "intents":incomingMessage["intents"],
                  "entities":incomingMessage["entities"]
                },
                {
                 "datetime":outgoingMessage["date"],
             	   "type":"outgoingMessage",
             	   "agent":"bot",
                 "text":outgoingMessage["text"]
                }
          ]}}
        }
    )


    updateUserSession(sessionId)
