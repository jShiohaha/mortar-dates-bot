import json
import os

from flask import Flask, request
from flask_injector import FlaskInjector
from injector import inject

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .src.constants.constants import BOT_NAME
from .src.dependencies import configure
from .src.store.clients import PyMongoClient, GraphMongoClient, GroupingMongoClient
from .src.response_generator import ResponseGenerator

app = Flask(__name__)

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id': os.getenv('GROUPME_BOT_ID'),
        'text': msg
    }
    request = Request(url, urlencode(data).encode())
    urlopen(request).read().decode()


def should_generate_response(data):
    msg_sender = data['name']
    msg = data['text']
    # ignore messages sent by the bot
    if msg_sender == BOT_NAME:
        return False
    # check if message first word references bot name, ignore @ sign
    msg_first_word = msg.split(" ")[0]
    if msg_first_word != "@{0}".format(BOT_NAME):
        return False
    return True

@inject
@app.route('/', methods=['POST'])
def webhook(generator: ResponseGenerator):
    data = request.get_json()
    if should_generate_response(data):
        response = generator.generate_response(data)
        if response is not None:
            send_message(response)
    return "OK", 200

@inject
@app.route('/', methods=['GET'])
def test(generator: ResponseGenerator):
    return generator.status(), 200

FlaskInjector(app=app, modules=[configure])
