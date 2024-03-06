import openai
from dotenv import load_dotenv
import os 
import sql
import sqlite3


load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


def general_response(text):
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
                        "content": text.replace('\n','')
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


def mood_score(user_id, group_id, text, mood,score):
    




def sum_user(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are a master of summarizing. You will summarize the user's text into three tags.Each tag is separated by commas. For example, ```tasks, jobs, promotions```, ```goal oriented, practice, portfolio```"""},
            {"role": "user", "content": text}
        ],
            temperature=0
        )
    return response.choices[0].message.content

def ans_question(title, question, user_id):
    conn = sqlite3.connect('src/db/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
    user = c.fetchone()
    conn.commit()
    conn.close()
    
    stream = openai.chat.completions.create(
            model="gpt-4-1106-preview", 
            messages=[
                {
                "role": "system",
                "content": f"""You are a professional at {user[2]}. You can think about this issue from a {user[2]} perspective. You can choose to search online to get more accurate information.  If you feel that the question I asked may not be so important, or there are other more important questions that I may not understand, you can try to guide me to further understand the relevant technical knowledge. 
                [INST]step by step think the RULE:
                1. you always follow user's language type.
                2. you always be kind.
                3. If you don't know the question, you should identify the user's qeustion.
                4. If you ensure that the user's question is not an knowledge question, you should guide the user to ask questions related to the {title}. and you only reply simple conclusion within 1 sentence. For example, "I think the most important thing is to understand the core issues."
                5. You should not answer questions that are irrelevant to the {title}. Instead, you should ask rhetorical questions to guide users to think about the core issues.
                6. Do not use Simplified Chinese. [/INST]"""
                },
                {
                    "role": "user",
                    "content": f"I'm a {user[3]} in this book club. My personality is {user[5]}. Please answer question '{question}' to fit my goal ```{user[4]}``` "
                }  
            ],
            max_tokens=1024,
            stream=True)
    return stream

    
        
        