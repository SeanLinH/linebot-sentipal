import openai
from dotenv import load_dotenv
import os 
import sql
import sqlite3
from api import prompts


load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


"""

features
1. one-sentence (1 dialog)
2. short-term (today)
    1. group memory
    2. personal memory
3. long-term (entire)
    1. chain 
    summarize each day's conversation
    2. chain every day's conversation

events
1. 

"""

def emergency(msg):
    response = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": prompts.concern()
                    },
                    {
                        "role": "user",
                        "content": str(msg)
                    }
                    
                ]
                )
    return response.choices[0].message.content

def reply(mem):
    msg = mem.split('\n')[-1]
    response = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": prompts.emotional_counseling()
                    },
                    {
                        "role": "user",
                        "content": f'My current question: {msg}. My past memroy: {mem}'
                    }
                    
                ]
                )
    return response.choices[0].message.content





def key_point(reply, msg):
    response = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": "You are a good keyword finder, and you only output 1 keypoint. You have to think step by step. What the context is the most important. You only output up to 5 words." # The symbol '+' in the middle of each keyword represents a separation. You can output up to 5 words"
                    },
                    {
                        "role": "user",
                        "content": reply.replace('\n','') + f"```question: {msg}```"
                    }
                    
                ]
                )
    return response.choices[0].message.content

def event_detector(group_mem):
    response = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": prompts.event_detect()
                    },
                    {
                        "role": "user",
                        "content": group_mem
                    }
                ]
                )
    return response.choices[0].message.content


def summarize(group_mem, events):
    response = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": prompts.summarize(events)
                    },
                    {
                        "role": "user",
                        "content": f"Please Summarize our conversations: {group_mem}"
                    }
                ]
                )
    return response.choices[0].message.content
    

# def mood_score(user_id, group_id, text, mood,score):
    




    
        
        