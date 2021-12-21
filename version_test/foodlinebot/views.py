from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pandas.core.base import DataError
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,ButtonsTemplate,
    PostbackEvent,PostbackTemplateAction,
    QuickReply,QuickReplyButton,PostbackAction,LocationAction,
    CarouselTemplate,CarouselColumn,LocationSendMessage
)

from .search import Toilet,Search,AED,Charger,T_bike
import configparser
config = configparser.ConfigParser()
config.read('constant.ini')

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method != 'POST':
        return HttpResponseBadRequest()


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
            
            if event.message.type=='location':
                global Search
                Search.my_lng = event.message.longitude
                Search.my_lat = event.message.latitude
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text = '定位設定成功',
                        quick_reply=QuickReply(
                            items = [QuickReplyButton(
                                        action=PostbackAction(
                                            label='開始查詢',
                                            text=None,
                                            data='開始查詢'
                                        )
                            )]
                        )
                    )
                )
            elif event.message.type!='text' or (event.message.text 
            not in config['constant']['key'].split(',')):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text = '定位設定成功後，就可以開始查詢囉!',
                        quick_reply=QuickReply(
                            items = [QuickReplyButton(
                                action=LocationAction(
                                    label="傳送位置")
                                    )]
                        )
                    )
                )
        
        elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
            if event.postback.data == "開始查詢": 
                targets = [('AED','AED','B'),('T_bike', 'T_bike','B'),('廁所', 'Toilet','A'),('充電樁', 'Charger','B')] # 如果target 不需要分類跳步驟B
                actions=[PostbackTemplateAction(label=target_Chin, text=target_Chin, data=f'{action}&{target_EN}') 
                        for target_Chin,target_EN,action in targets]
              
                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='選擇想要查詢的項目',
                            text='選項',
                            actions=actions
                        )
                    )
                )
            elif event.postback.data[0:1] == "A": 
                target = event.postback.data[2:]  
                toilet_classes = [('男廁','male'),('女廁', 'female'),('無障礙廁所', 'accessible')]

                line_bot_api.reply_message(   
                    event.reply_token,
                    TextSendMessage(
                        text = '選擇廁所分類',
                        quick_reply=QuickReply(
                            items = [QuickReplyButton(action=PostbackAction(label=classes_Chin, text=classes_Chin,
                                    data=f'B&{target}&{classes_EN}' )) for classes_Chin,classes_EN in toilet_classes]
                        )
                    )
                )


            elif event.postback.data[0:1] == "B":
                target_category = event.postback.data[2:].split('&')
                if len(target_category) == 2:
                    food = Toilet(target_category[0],target_category[1]) # 建立物件 參數為剛剛button template 所點的選項

                elif (len(target_category) == 1 and target_category[0] == 'AED'):
                    food = AED(target_category[0],None)

                elif (len(target_category) == 1 and target_category[0] == 'Charger'):
                    food = Charger(target_category[0],None)
                    
                elif (len(target_category) == 1 and target_category[0] == 'T_bike'):
                    food = T_bike(target_category[0],None)
                columns=[CarouselColumn(
                            title=f'路徑{i}',
                            text=food.nearbytarget_info(i),
                            actions=[PostbackTemplateAction(
                                        label='立即前往',
                                        text='立即前往',
                                        data = f'C&{food.nearbytarget_lng(i)}&{food.nearbytarget_lat(i)}&{food.nearbytarget_address(i)}'
                                        )]
                            )for i in range(1,6)] # 前五近資料的CarouselColumn 與 其回傳值'參數'

                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Carousel template',
                        template=CarouselTemplate(
                            columns=columns
                        )
                    )
                )
            
            elif event.postback.data[0:1] == "C":
                data = event.postback.data[2:].split('&')
                lng,lat,add = float(data[0]),float(data[1]), data[2]
                line_bot_api.reply_message(
                    event.reply_token,
                    LocationSendMessage(
                        title='目標地點',
                        address=add, 
                        latitude=lat, 
                        longitude=lng))

    return HttpResponse()

