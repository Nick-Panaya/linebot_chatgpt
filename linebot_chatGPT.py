from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "72d27a74ef2dba7b55c58aad2f376b4f"
channel_access_token = "vOqyNSLJdLL7f6tnx/OH9xQnPzcGvRgTKJLJFmYcqtvZAdL7GpXI5Q+3M0pzxvstM+rM9bAc+hl+Up6QkeKEO6SYj6jGVpuaY8IGzk1VktofprHsOcneAU5Kt3xta2vIOZ0Wl3OlrpJ5n2xZzo686QdB04t89/1O/w1cDnyilFU="

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

