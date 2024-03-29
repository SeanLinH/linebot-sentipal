
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
from src.prisma import glog, create_one_mood, Mood, delete_user_moods, create_one_response, Response, query_user_memory, query_group_memory,query_all_group_memory, update_one_user, register_user_api, clr_Green, clr_Red, clr_Yellow, clr_Cyan, clr_Off
from api.huggingface import Models
from api.LangchainGPT import Router, computeMoodScore, report, Require
from api import prompts, ChatGPT


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

    if 'SentiPal' in reply_msg or 'sentipal' in reply_msg:
        return '\n\n很高興認識你! 這是我的網站: https://sentipal.live '
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
    if json_data.get("events") == None:
        glog(f'{clr_Red}Not accept data format (1){clr_Off}')
        return
    if len(json_data['events']) == 0:
        glog(f'{clr_Red}Not accept data format (2){clr_Off}')
        return
    # glog(json_data)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LINE_BOT_KEY = os.getenv("LINEBOT_KEY")
    LINE_SECRET_KEY = os.getenv("LINE_SECRET_KEY")
    print(LINE_SECRET_KEY)
    try:
        openai.api_key = OPENAI_API_KEY
        line_bot_api = LineBotApi(LINE_BOT_KEY)
        handler = WebhookHandler(LINE_SECRET_KEY)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message'].get('text') + '\n' #使用者個對話
        ai_msg = msg[:1]  #咒語
        user = json_data["events"][0]["source"]["userId"]
        group = json_data["events"][0]["source"].get("groupId")
        print(user)
        # 取出文字的前五個字元，轉換成小寫
        reply_msg = ''
        glog(f'{user}: {clr_Green}{msg}{clr_Off}')

        if msg in ['/caregiver', '/case', '/general']:
            """Update user的 role 角色"""
            await update_one_user(
                user_id=user,
                data={
                    'user_role': msg[1:]
                }
            )
            ext_message = TextSendMessage(text='role') ## 測試回覆
            line_bot_api.reply_message(tk,text_message)
            return
            

        elif msg[:3] == '/註冊':
            """更新user api"""
            API_KEY = msg[3:]
            register_user_api(user, API_KEY)
            ext_message = TextSendMessage(text='註冊') ## 測試回覆
            line_bot_api.reply_message(tk,text_message)
            return
            
        elif msg[:8] == '/summary':
            if group == None:
                total, mem = await query_user_memory(user, days=2)
            else:
                total, mem = await query_all_group_memory(group, days=2)
            glog(f'user_id:{user} mem =>\n\ttotal:{clr_Yellow}{total}{clr_Off}\n\tmem:{clr_Yellow}{mem}{clr_Off}')
            events = ChatGPT.event_detector(mem)
            print(events)
            response = ChatGPT.summarize(mem, events)
            text_message = TextSendMessage(text=response)
            line_bot_api.reply_message(tk,text_message)
            return
        
            
        elif msg[:7] == '/remove':
            total = await delete_user_moods(user_id=user)
            text_message = TextSendMessage(text='Your record has been cleared!')
            line_bot_api.reply_message(tk,text_message)
            glog(f'There are {total} mood records has been deleted!')
            return
        

        
        print('huggingface....')
        hf = Models(msg)
        hf = Models(hf.translate())
        user_mood = hf.go_emotion() # mood classification
        sentiment = hf.postive_or_negative()
        mood_score = hf.detect_depression()
        # statble_score = 0
    

        newMood = await create_one_mood(Mood(
            user_id=user,
            group_id=group,
            user_text=msg,
            user_mood=user_mood,
            mood_score=mood_score,
            # stable_score= statble_score
            ))
        glog(mood_score)
        glog(f'[LINE API call] +{clr_Yellow}line_bot_api.get_profile({clr_Cyan}{user}{clr_Yellow}){clr_Off}')
        # profile = line_bot_api.get_profile(user)
        # glog(f'[LINE API call] -{clr_Yellow}line_bot_api.get_profile({clr_Cyan}{user}{clr_Yellow}){clr_Off} ... profile.display_name => {clr_Cyan}{profile.display_name}{clr_Off}')

        if group == None:
            total, mem = await query_user_memory(newMood.user_id, days=7)
            glog(f'{clr_Yellow}User memory ...{clr_Off}\n\tuser_id:{newMood.user_id} mem =>\n\ttotal:{clr_Yellow}{total}{clr_Off}\n\tmem:{clr_Yellow}{mem}{clr_Off}')
        else:
            total, mem = await query_group_memory(
                group_id=newMood.group_id, 
                user_id=newMood.user_id, 
                includeResponse=False,
                days=7)
            glog(f'{clr_Yellow}Group memory ...{clr_Off}\n\tgroup_id:{newMood.group_id} mem =>\n\ttotal:{clr_Yellow}{total}{clr_Off}\n\tmem:{clr_Yellow}{mem}{clr_Off}')
        
        # if mood_score == 1:
        #     factor = hf.classifer('individual', 'relationship', 'community interact', 'society culture')
        #     statble_score = int(computeMoodScore(mem, user_mood, sentiment, mood_score))

        
        if (sentiment == -1 or mood_score == 1) and user_mood in ['sadness','disappointment','annoyance', 'anger', 'grief', 'fear', 'disgust', 'remorse', 'desire']:
            print("自動關懷")
            response = ChatGPT.emergency(msg)
            await create_one_response(Response(user_id=user, group_id=group, ai_text=response),aimTo=newMood)
            text_message = TextSendMessage(text=f'嘿！\n{response}')
            line_bot_api.reply_message(tk,text_message)

        elif msg[:5] in ['/心情報告', '/情緒指數', '/心情分數','/情緒分數', '/報告']:
            """Langchain 方式來做"""
            # profile = line_bot_api.get_profile(user)
            response = report(mem)
            key_point = ChatGPT.key_point(response, "")
            url = search_google(key_point, "")
            await create_one_response(Response(user_id=user, group_id=group, ai_text=response),aimTo=newMood)
            text_message = TextSendMessage(text=f'Hello! 你好！\n以下是你的心情報告\n\n{response}\n{url}')
            line_bot_api.reply_message(tk,text_message)
            return

        
        elif msg[0] =='/':
            # 訊息發送給 OpenAI
            print('啟動咒語...')
            
            reply_msg = ChatGPT.reply(mem)
            
            key_point = ChatGPT.key_point(reply_msg, msg)
            
            glog(key_point)
            url = search_google(key_point + '. ' + msg, reply_msg)
            await create_one_response(Response(user_id=user, group_id=group, ai_text=reply_msg),aimTo=newMood)
            
            text_message = TextSendMessage(text=f'{reply_msg} {url}')
            line_bot_api.reply_message(tk,text_message)
        
    except Exception as e:
        glog(f"{clr_Red}{e}{clr_Off}")

if __name__ == "__main__":
    # run_with_ngrok(app)   # colab 使用，本機環境請刪除
    app.run()
