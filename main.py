from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, abort
from datetime import datetime
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,AudioSendMessage
from lib.ClireaFramework import *
from google.cloud import storage
import hmac
import base64
import hashlib
import os
from linebot_demo import linebot_demo
cipher = AESCipher()


app = Flask(__name__)
app.secret_key = ChannelSecret

@app.route('/', methods=['POST'])
def main():
        
        line_bot_api = LineBotApi(ChannelAccessToken)
        parser = WebhookParser(ChannelSecret)
        body = request.get_data(as_text=True)
        hash = hmac.new(ChannelSecret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash).decode()

        if signature != request.headers['X_LINE_SIGNATURE']:
            return abort(405)
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return abort(405)

        for event in events:
            if not isinstance(event, MessageEvent):
                continue    
            return linebot_demo(event,line_bot_api)
            





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))