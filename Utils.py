import requests
import json
from User import User
import urllib.parse
import urllib.request
import re
import random
from linebot.models import *
from Config import Config

class Utils:
    def __init__(self, config: Config):
        self.config = config
    def query_dialogue(self, user: User, text: str):
        def query(url: str, payload):
            response = requests.post(url, headers=self.config.headers, json=payload)
            return response.json()
        payload = {
            "inputs": {
                "past_user_inputs": user.past_user_inputs,
                "generated_responses": user.generated_responses,
                "text": text
            },
        }
        print(payload, flush=True)
        generated_text =  query(self.config.DIALOGUE_MODEL_API_URL, payload)['generated_text']
        user.record_user_input(text)
        user.record_responses(generated_text)
        # user.generated_responses.append(generated_text)
        # user.past_user_inputs.append(text)
        reply_msg = TextSendMessage(text=generated_text)
        return reply_msg
    def query_image(self, user: User, img_path: str):
        def query(filename):
            with open(filename, "rb") as f:
                data = f.read()
            response = requests.request("POST", self.config.IMG_MODEL_API_URL, headers=self.config.headers, data=data)
            return json.loads(response.content.decode("utf-8"))
        output = query(img_path)
        if len(output) == 0:
            msg = 'Sorry, I wasn\'t able to identify anything in this picture.'
        elif len(output) == 1:
            msg = f"It is a {output[0]['label']}"
        else:
            msg = "I found"
            for item in output[:-1]:
                msg += f" {item['label']},"
            msg += f' and {output[-1]["label"]} in this picture.'
        reply_msg = TextSendMessage(text=msg)
        return reply_msg
