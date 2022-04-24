from linebot.models import *
class Config:
    def __init__(self):
        self.API_TOKEN = "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"
        self.DIALOGUE_MODEL_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        self.IMG_MODEL_API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
        self.headers = {"Authorization": f"Bearer {self.API_TOKEN}"}
        self.stickers = {
            446: list(range(1988, 2028)),
            789: list(range(10855, 10895)),
            1070: list(range(17839, 17879)),
            6136: list(range(10551376, 10551400))
        }
        self.QA = {
            "Tell me about your creator.": "Sure.\nHe is Chang-Yuan Lo, an interviewee of Line Tech Fresh 2022 - Data dev",
            "How to perform image recognition?": "Send me some images, I would do the work for you :D",
            "What can you do?": "I can perform image recognition and carry some simple conversation :D",
            "?": "Try out some options below :D"
        }
        self.quick_reply = QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="About me", text="Tell me about your creator.")
                ),
                QuickReplyButton(
                    action=MessageAction(label="???", text="How to perform image recognition?")
                ),
                QuickReplyButton(
                    action=MessageAction(label="What can you do?", text="What can you do?")
                )
            ]
        )
        # self.image_recognition_model_url = 
        # https://huggingface.co/facebook/detr-resnet-50 
    def gen_greeting_message(self, username: str) -> str:
        msg = f"Hello, {username}.\nNice to meey you.\n" + \
            "I am Image Recognition Bot,\n" + \
                "You can chat with me or send me some images,\n" + \
                    "I could identify the objects in the image :D\n" + \
                        "Enter \'?\' for hints."
        return msg