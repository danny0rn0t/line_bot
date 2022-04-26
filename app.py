from flask import Flask, request, abort
from flask_caching import Cache 

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from Utils import Utils
from User import User
from Config import Config
from line_token import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET
import tempfile
import random


app = Flask(__name__)
cache = Cache()
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})
cache.delete("users_data")
config = Config()
utils = Utils(config)

# Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    print(type(profile), flush=True)
    print(profile, flush=True)
    msg = config.gen_greeting_message(username=profile.display_name)
    reply_msg = TextSendMessage(text=msg, quick_reply=config.quick_reply)
    line_bot_api.reply_message(event.reply_token, reply_msg)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    package_id = random.choice(list(config.stickers.keys()))
    sticker_id = random.choice(config.stickers[package_id])
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=str(package_id),
            sticker_id=str(sticker_id))
    )

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text in config.QA:
        reply_msg = TextSendMessage(text=config.QA[event.message.text], quick_reply=config.quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_msg)
    else:
        user_id = event.source.user_id
        users_data = cache.get("users_data")
        if not users_data:
            users_data = {}
        if user_id not in users_data:
            users_data[user_id] = User(user_id)
        user = users_data[user_id]
        reply_msg = utils.query_dialogue(user, event.message.text)
        line_bot_api.reply_message(event.reply_token, reply_msg)
        cache.set("users_data", users_data)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    user_id = event.source.user_id
    users_data = cache.get("users_data")
    if not users_data:
        users_data = {}
    if user_id not in users_data:
        users_data[user_id] = User(user_id)
    user = users_data[user_id]

    img_tmp_dir = '/tmp/images/'
    try: 
        os.makedirs(img_tmp_dir)
    except:
        pass
    ext = 'jpg'
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=img_tmp_dir, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    full_path = img_tmp_dir + dist_name
    # print(full_path, flush=True)
    reply_msg = utils.query_image(user, full_path)
    line_bot_api.reply_message(event.reply_token, reply_msg)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #https://api-inference.huggingface.co/models/microsoft/DialoGPT-large/api_FaTThXjiOcMNrzITNPyQCjxgZhTsNEgjpB
