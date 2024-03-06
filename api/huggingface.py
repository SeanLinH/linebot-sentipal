import requests
import os
from dotenv import load_dotenv
load_dotenv()

HF_KEY = os.environ.get("HF_API_KEY")


class Models:
    def __init__(self, text):
        self.text = text
        

    def detect_depression(self):
        API_URL = "https://api-inference.huggingface.co/models/ShreyaR/finetuned-roberta-depression"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        
        def query(payload):
        	response = requests.post(API_URL, headers=headers, json=payload)
        	return response.json()
        	
        output = query({
        	"inputs": self.text,
        })
        return output

    def go_emotion(self):
        API_URL = "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        
        def query(payload):
        	response = requests.post(API_URL, headers=headers, json=payload)
        	return response.json()
        	
        output = query({
        	"inputs": self.text,
        })
        return output

    def translate(self):
        API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-zh-en"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        
        def query(payload):
        	response = requests.post(API_URL, headers=headers, json=payload)
        	return response.json()
        	
        output = query({
        	"inputs": self.text,
        })
        return output
        


