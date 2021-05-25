# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:46:43 2021

@author: ruanr
"""

import flask
from flask import request, make_response, abort
from botkit import sendToBotkit
from zenvia import sendToZenvia
from functools import wraps 

#from mongo import addEvent, incomingMessageMongo, outgoingMessageMongo


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'sabemi' and auth.password == '=2VeSDy!v3M!wmwFEXSZ#TPX7dM22WF^s7wkZGXCZuf4MxgP@wrn9UX_3FGZ^*cp':
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated


app = flask.Flask(__name__)


@app.route('/message', methods=['GET'])
def heartbeat():
    print("tudum")
    return({"tudum":"tudum"})

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

    #incomingMessageMongo(message,userNumber)
    replyFromBotkit = sendToBotkit(message,userNumber)
    #print(replyFromBotkit)
    #addEvent(replyFromBotkit)
    statusFromZenvia = sendToZenvia(replyFromBotkit,botNumber, userNumber)
    #outgoingMessageMongo(statusFromZenvia)

    #for message in statusFromZenvia:
    #  print("\n",message["text"])
    return ""


@app.route('/transcription', methods=['GET'])
@auth_required
def getTranscription():
  user = request.args.get('user')
  if(user=="123456789"):

    return({
      "datetimeStart": "Wed May 19 2021 13:02:10 GMT-0300",
      "datetimeFinish": "Wed May 19 2021 13:03:03 GMT-0300",
      "user": {
        "id": "123456789",
        "name": "João da Silva"
      },
      "sessionId": "435d1f64-cce2-5ee7-ed23-0be59fe1bde7",
      "lgpd": "true",
      "transfered": "false",
      "convertFinancialAssistance": "true",
      "convertInsurance": "false",
      "events": [
        {
          "id": "1",
          "datetime": "Wed May 19 2021 13:02:10 GMT-0300",
          "type": "createIteraction",
          "agent": "middleware",
          "parentId": None
        },
        {
          "id": "2",
          "datetime": "Wed May 19 2021 13:02:11 GMT-0300",
          "type": "outgoingMessage",
          "section": "pre-simulation",
          "parentId": "1",
          "agent": "bot",
          "text": "Olá, João,  eu sou a *Sol*, especialista de Crédito da Sabemi 🙋‍♀️. Tenho uma solução personalizada para você tirar seus planos do papel e realizar seus sonhos"
        },
        {
          "id": "3",
          "datetime": "Wed May 19 2021 13:02:11 GMT-0300",
          "type": "outgoingMessage",
          "section": "pre-simulation",
          "parentId": "2",
          "agent": "bot",
          "text": "Se quiser saber mais, para segurança dos seus dados, preciso garantir que estou falando com a pessoa certa\n\n *João da Silva*, é você mesmo?😊\n\nDigite *Sim*, se for você\n\nDigite *Não*, se você não conhecer essa pessoa"
        },
        {
          "id": "4",
          "datetime": "Wed May 19 2021 13:02:19 GMT-0300",
          "type": "incomingMessage",
          "section": "pre-simulation",
          "parentId": "3",
          "agent": "user",
          "text": "sim"
        },
        {
          "id": "5",
          "datetime": "Wed May 19 2021 13:02:20 GMT-0300",
          "type": "outgoingMessage",
          "section": "pre-simulation",
          "parentId": "4",
          "agent": "bot",
          "text": "Que bom! Agora você esta um passo mais próximo de realizar seus sonhos! 🤩\n\nE para que eu possa apresentar uma proposta na medida, vou precisar que você me informe alguns dos seus dados pessoais.\n\nMas vale ressaltar: *este é um ambiente seguro* e seus dados estão protegidos e guardados, tudo de acordo com a *Lei Geral de Proteção de Dados* (LGPD) e *Direito do Consumidor* 🔒"
        },
        {
          "id": "6",
          "datetime": "Wed May 19 2021 13:02:20 GMT-0300",
          "type": "outgoingMessage",
          "section": "pre-simulation",
          "parentId": "5",
          "agent": "bot",
          "text": "Se quiser saber mais, é só clicar nesse link para acessar nossas políticas e termos sobre a Lei Geral de Proteção de dados: 👉🏼 https://www.sabemi.com.br/politica-de-privacidade"
        },
        {
          "id": "7",
          "datetime": "Wed May 19 2021 13:02:21 GMT-0300",
          "type": "outgoingMessage",
          "section": "pre-simulation",
          "parentId": "6",
          "agent": "bot",
          "text": "Vamos lá!? Me conta qual é o seu *nome completo*?"
        }
      ]
    })
  else:
    abort(404, description="Transcription not found")
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3001)

