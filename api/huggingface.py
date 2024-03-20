import requests
import os
from dotenv import load_dotenv
load_dotenv()
import time

HF_KEY = os.environ.get("HF_API_KEY")


class Models:
    def __init__(self, text):
        self.text = text[:512]

        self.pnn = {'positive': -1,
                      'neutral': 0, 
                      'negative': 1,
                       None: None}
        self.det_lab = {'LABEL_0': 0,
                       'LABEL_1': 1, 
                       None:None}
    

    def detect_depression(self):
        """判斷文字是否為憂鬱傾向"""
        API_URL = "https://api-inference.huggingface.co/models/ShreyaR/finetuned-roberta-depression"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        
        def query(payload):
        	response = requests.post(API_URL, headers=headers, json=payload)
        	return response.json()
        	
        output = query({
        	"inputs": self.text,
        })
        
        
        try:
            print(output[0][0].get('label'))
            return self.det_lab.get(output[0][0].get('label'))
        except:
            print("reconnect detect_depression")
            time.sleep(2)
            return self.detect_depression()

    def go_emotion(self):
        """將文字標記為情緒類別--> user_mood"""
        API_URL = "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        
        def query(payload):
        	response = requests.post(API_URL, headers=headers, json=payload)
        	return response.json()
        	
        output = query({
        	"inputs": self.text,
        })
        
        try:
            print(output[0][0].get('label'))
            return output[0][0].get('label')
        except:
            print("reconnect go_emotion")
            time.sleep(2)
            return self.go_emotion()

    def translate(self):
        """將文字中翻英"""
        API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-zh-en"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        
        def query(payload):
        	response = requests.post(API_URL, headers=headers, json=payload)
        	return response.json()
        	
        output = query({
        	"inputs": self.text,
        })
        
        try:
            print(output[0].get('translation_text'))
            return output[0].get('translation_text')
        except:
            print("reconnect translate")
            time.sleep(2)
            return self.translate()
    
    
    def classifer(self, *args):
        """給定特定的文字類別，可自定義"""
        API_URL = "https://api-inference.huggingface.co/models/amaye15/Stack-Overflow-Zero-Shot-Classification"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        print(args)
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        
        output = query({
            "inputs": self.text,
            "parameters": {"candidate_labels": list(args)},
        })
        try:
            print(output.get('labels')[0])
            return output.get('labels')[0]
        except:
            print("reconnect classifer")
            time.sleep(2)
            return self.classifer()
            

    
    def postive_or_negative(self):
        """mood_score  [-1, 0, 1]"""
        API_URL = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        
        
        def query(payload):
        	response = requests.post(API_URL, headers=headers, json=payload)
        	return response.json()
        	
        output = query({
        	"inputs": self.text,
        })

        try:
            print(output[0][0].get('label'))
            return output[0][0].get('label')
        except:
            print("reconnect postive_or_negative")
            time.sleep(2)
            return self.postive_or_negative()


