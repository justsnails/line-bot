from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='71RF0Xz+5AL2bMKGWke15pQSG0tIrIcvnEK0qegrz/QmTuidHTsB7xbLd9VdE5D5c9hZinnR3Z21pXU0txPqjpq2M4a9HNalVNlSXbash7mJSfUT0GdhRXHzPCGJh578wJe0SPCTyeLkP9pKC0z85QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2622d98b7cced2f35f88b6043770feb0')


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        msg = event.message.text
        r = '我看不懂你說什麼'
        if msg in ['hi', 'Hi', 'HI', 'hI']:
            r = '嗨'
        elif msg in ['你是誰', '妳是誰']:
            r = '我是機器人'
        elif '訂位' in msg:
            r = '你想訂位，是嗎?'
        elif msg == '你吃飯了嗎':
            r = '還沒，有推薦的嗎?'
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=r)]
            )
        )
if __name__ == "__main__":
    app.run()