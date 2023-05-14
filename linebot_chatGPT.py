from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "13f465950c9ac3f1800c00160d16007e"
channel_access_token = "5wiOP1ZmVkmJDEP9m/zgbo+EqIKo01Pqn8HlnIpr0dLogrQS9kdjNLi3bUmdpxMqrnWjOkf/kmOJ9vegnS0mhuyjCCMqpPGBK64F5l5wt3UruHg1WDClZv43meHeqkAHvPRJhH4hL23ATEQ/xy83zwdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

