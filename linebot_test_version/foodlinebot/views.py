from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    QuickReply,MessageAction,QuickReplyButton,PostbackAction,LocationAction
)
 
from .search import Toilet
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
 
                if event.message.text == '哈囉':
 
                    line_bot_api.reply_message(  # 回復「選擇地區」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇地區',
                                actions=[
                                    PostbackTemplateAction(
                                        label='哺乳室',
                                        text='哺乳室',
                                        data='A&哺乳室'
                                    ),
                                    PostbackTemplateAction(
                                        label='飲水機',
                                        text='飲水機',
                                        data='A&飲水機'
                                    ),
                                    PostbackTemplateAction(
                                        label='廁所',
                                        text='廁所',
                                        data='A&toilet'
                                    ),
                                    PostbackTemplateAction(
                                        label='充電樁',
                                        text='充電樁',
                                        data='A&充電樁'
                                    )
                                ]
                            )
                        )
                    )
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
 
                if event.postback.data[0:1] == "A":  # 如果回傳值為「選擇地區」
 
                    target = event.postback.data[2:]  # 透過切割字串取得地區文字
 
                    line_bot_api.reply_message(   # 回復「選擇美食類別」按鈕樣板訊息
                        event.reply_token,
                        TextSendMessage(
                            text = '選擇廁所分類',
                            quick_reply=QuickReply(
                                items = [
                                     QuickReplyButton(
                                         action=PostbackAction(
                                            label='男廁',
                                            text='男廁',
                                            data=f'B&{target}&male')
                                         
                                     ),
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            label="女廁",
                                            text="女廁",
                                            data=f'B&{target}&female')
                                    ),
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            label="無障礙廁所",
                                            text="無障礙廁所",
                                            data=f'B&{target}&accessible')
                                    ),
                                    QuickReplyButton(
                                    action=LocationAction(label="傳送位置")
                                    ),
                                ]
                            )
                        )
                    )
 
                elif event.postback.data[0:1] == "B":  # 如果回傳值為「選擇美食類別」
 
                    result = event.postback.data[2:].split('&')  # 回傳值的字串切割
 
                    food = Toilet(result[0],result[1])
 
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=food.nearby_target())
                        # TextSendMessage(text="有回覆")
                    )
 
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
