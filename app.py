# -*- coding: utf-8 -*-
import subprocess
import os
import json

from bottle import post, request, run, hook, template, route, get
from pymessenger.bot import Bot

@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def _search(query):
    """
    Search method
    """
    q = 'howdoi {}'.format(query)
    p = subprocess.Popen(q, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=True)
    output, error = p.communicate()
    if error:
        return error

    output = "```\n{}```".format(output)
    return output


@get('/howdoi')
def howdoi():
    """
    Example:
        /howdoi open file python
    """
    # text = request.forms.text
    text = request.query.text
    if not text:
        return 'Please type a ?text= param'

    output = _search(text)
    # formatting
    return output

@get('/webhook')
def webhook():
    if 'hub.mode' in request.query and request.query['hub.mode'] == "subscribe":
        challenge = request.query['hub.challenge']
        return challenge
    else:
        return 'null'

@post('/webhook')
def webhook():
    body = json.load(request.body)
    print body

    bot = Bot('EAAJudOVDEOYBAOYJVj7sRGXnv4S5MaFrjSJjN8SZCHB269BQk7GUTzZCE8ZCrRpOv97ZC3wbVSzww3eYfpjRCPfBrmUZCHrouSj9M2M1ZAYqIJKxzXfrnfM7g8zeliyGdrl7BcnIftYZAsPQD3WZA2pRDcNM85ToJTCPjQ1cAQdgsQZDZD')

    for entry in body['entry']:
        for message in entry['messaging']:
            if 'text' in message['message']:
                recipient_id = message['sender']['id']
                question = message['message']['text']
                answer = _search(question)
                bot.send_text_message(recipient_id, answer)

    return None

@route('/')
def index():
    return template('index')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', False)
    run(host='0.0.0.0', port=port, debug=debug)
