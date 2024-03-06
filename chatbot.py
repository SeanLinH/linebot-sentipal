
import openai
import requests
# from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
from dotenv import load_dotenv
import os
import asyncio
from src.prisma import glog, create_one_mood, Mood, delete_user_moods, create_one_response, Response, query_user_memory,clr_Green, clr_Red, clr_Yellow, clr_Off

load_dotenv()


# search something from google
def search_google(query, reply_msg):
    url = "https://www.google.com/search?q={}&gl=tw".format(f"{reply_msg} + {query} lang:tw,en")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.text
    text = text[text.find('id="search"'):]
    text = text[text.find('<a jsname'):]
    text = text[text.find('href')+6:]
    text = text[:text.find('"')]

    if 'Sean' in reply_msg or '士桓' in reply_msg:
        return '\n\n很高興認識你! 這是我的LinkedIn:https://www.linkedin.com/in/seanlin-tw'
    elif 'http' not in text:
        return ''
    elif str(response) == "<Response [429]>":
        return '\n\n我累了🥵, 休息一下喝口水'
    return '\n\n幫你找找:' + text


app = Flask(__name__)
@app.route("/", methods=['POST'])
def linebot_endpont():
    asyncio.run(linebot())
    return 'OK'

async def linebot() -> None:
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    glog(json_data)
    API_KEY = os.getenv("OPENAI_API_KEY")
    LINE_BOT_KEY = os.getenv("LINEBOT_KEY")
    LINE_SECRET_KEY = os.getenv("LINE_SECRET_KEY")
    try:
        openai.api_key = API_KEY
        line_bot_api = LineBotApi(LINE_BOT_KEY)
        handler = WebhookHandler(LINE_SECRET_KEY)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text'] + '.'
        ai_msg = msg[:1]
        user = json_data["events"][0]["source"]["userId"]
        group = json_data["events"][0]["source"]["groupId"]
        # 取出文字的前五個字元，轉換成小寫
        reply_msg = ''
        glog(f'{user}: {clr_Green}{msg}{clr_Off}')
        newMood = await create_one_mood(Mood(
            user_id=user,
            group_id=group,
            user_text=msg
            ))
        
        if msg[:6] == 'remove':
            total = await delete_user_moods(user_id=user)
            text_message = TextSendMessage(text='Your record has been cleared!')
            line_bot_api.reply_message(tk,text_message)
            glog(f'There are {total} mood records has been deleted!')
        elif ai_msg =='/':
            # text_message = TextSendMessage(text='今天陪貓咪玩耍時，踢到桌腳🥲，我現在在檢查，等等回去時再陪你。\n我順便再抓個臭蟲，通個水管。')
            # line_bot_api.reply_message(tk,text_message)

            # with open(f'log/record.txt', 'a') as ff:
            #     ff.write(msg[1:] + '\n')
            #     ff.close()
                
            
            total, mem = await query_user_memory(newMood.user_id)
            glog(f'user_id:{newMood.user_id} mem =>\n\ttotal:{clr_Yellow}{total}{clr_Off}\n\tmem:{clr_Yellow}{mem}{clr_Off}')
            # 訊息發送給 OpenAI
            response = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.9,
                messages=[
                    {
                    "role": "system",
                    "content": "You are a good psychological counselor. You can predict whether a patient has a tendency to be depressed from the words he or she chats with. You can judge the user’s depression mood index for each chat, ranging from 0 to 10. The higher the value, the higher the risk of depression. ."
                    },
                    {
                        "role": "user",
                        "content": mem
                    }  
                ]
                )
            
            # 接收到回覆訊息後，移除換行符號
            reply_msg = response.choices[0].message.content

            key_point = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": "You are a good keyword finder, and you only output 1 keypoint. You have to think step by step. What the context is the most important. You only output up to 5 words." # The symbol '+' in the middle of each keyword represents a separation. You can output up to 5 words"
                    },
                    {
                        "role": "user",
                        "content": reply_msg.replace('\n','') + f"```question: {msg}```"
                    }
                    
                ]
                )
            
            glog(key_point.choices[0].message.content)
            url = search_google(key_point.choices[0].message.content + '. ' + msg, reply_msg)

            await create_one_response(Response(user_id=user, group_id=group,ai_text=reply_msg),aimTo=newMood)

            text_message = TextSendMessage(text=reply_msg + url)
            line_bot_api.reply_message(tk,text_message)
        
    except Exception as e:
        glog(f"{clr_Red}{e}{clr_Off}")

if __name__ == "__main__":
    # run_with_ngrok(app)   # colab 使用，本機環境請刪除
    asyncio.run(app.run())
