# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 15:15:40 2021

@author: NUTC
"""

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('mFHBX3j2Ffp3+6e0ayfsyJXMt8gHE4wpqpB7UZ1+aZgU43B/1GXeCUXwFwu0VOZLj4mZRS2vrMj2w+EDlZjKlsS3EEmba1HaZK9WysM5LiN4nevtq8mEDBJbojPHT8zCCB2xC4he04uW5q6cDBB78gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1a70c4e4de23b490acd3c11c685dde1a')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()