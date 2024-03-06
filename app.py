
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
from api import ChatGPT
from api.huggingface import Models

load_dotenv()


# search something from google
def search_google(query):
    url = "https://www.google.com/search?q={}&gl=tw".format(f"{query} lang:tw,en")
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

    if 'http' not in text:
        return ''
    elif str(response) == "<Response [429]>":
        return '\n\n我累了🥵, 休息一下喝口水'
    return '\n\n幫你找找:' + text


app = Flask(__name__)
@app.route("/", methods=['POST'])
def linebot():

    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    # print(json_data)
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
        user = json_data["events"][0]["source"]["userId"]
        group = json_data["events"][0]['source'].get('groupId')
        hf = Models(msg)
        mood = hf.go_emotion()
        mood_score = hf.detect_depression()
        
        print(mood[0][0]['label'], mood_score[0][0]['label'])
        
        ai_msg = msg[:1] #啟動咒語
        
        # 取出文字的前五個字元，轉換成小寫
        reply_msg = ''
        # print(f'{user}: {msg}')
        with open(f'log/{user}.txt', 'a') as f:
            f.write(msg)
            if ai_msg == '/':
                f.write('####')
            f.close()
        
        mem = open(f'log/{user}.txt', 'r').read()

        if len(mem) > 2000:
            with open(f'log/{user}.txt', 'w') as f:
                f.write(mem[-2000:])
                f.close()
            mem = mem[-2000:]

        
        if msg[:6] == 'remove':
            open(f'log/{user}.txt', 'w').write("")
            text_message = TextSendMessage(text='Your record has been cleared!')
            line_bot_api.reply_message(tk,text_message)
            print('cleared!!')
        elif ai_msg =='/':
            # text_message = TextSendMessage(text='今天陪貓咪玩耍時，踢到桌腳🥲，我現在在檢查，等等回去時再陪你。\n我順便再抓個臭蟲，通個水管。')
            # line_bot_api.reply_message(tk,text_message)

            # with open(f'log/record.txt', 'a') as ff:
            #     ff.write(msg[1:] + '\n')
            #     ff.close()
                
            
            
            with open(f'log/record.txt', 'a') as ff:
                ff.write(msg + '\n')
                ff.close()
        
            

            # 接收到回覆訊息後，移除換行符號
            reply_msg = ChatGPT.general_response(mem)        
            key_point = ChatGPT.key_point(reply_msg, msg)
            # print(key_point)
            
            url = search_google(f"{key_point} and {msg}")

            with open(f'log/{user}.txt', 'w') as f:
                f.write(mem + reply_msg + '\n')
                f.close()

            text_message = TextSendMessage(text=reply_msg + url)
            line_bot_api.reply_message(tk,text_message)
        
    except Exception as e:
        print(e)
    return 'OK'

if __name__ == "__main__":
    # run_with_ngrok(app)   # colab 使用，本機環境請刪除
    app.run()
