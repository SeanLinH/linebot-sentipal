from langchain.memory import ConversationSummaryBufferMemory, ConversationBufferWindowMemory, ChatMessageHistory 
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.chains.router import MultiPromptChain
# from langchain.chains.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import ResponseSchema
# from langchain_openai import ChatOpenAI


import os 
import sqlite3
import openai
from dotenv import load_dotenv

# from api 
from api import prompts

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0.7, model="gpt-4-0125-preview",api_key=os.environ.get("OPENAI_API_KEY"))

"""
1. Requirement
2. Knowledge
3. Search
4. Common sense
5. 
"""

def Require(history):
    prompt = ChatPromptTemplate.from_template(template=prompts.emotional_counseling())
    chat = LLMChain(llm=llm, prompt=prompt)
    print(history.messages)
    response = chat(history.messages)

    
    return response.content
    


def Router(text):
    """暫時先棄用"""
    prompt_infos = [
        {
            "name": "friend_smalltalk", 
            "description": "Good for answering at closed friend", 
            "prompt_template": prompts.friend_smalltalk()
        },
        {
            "name": "emotional_counseling", 
            "description": "Good for answering emotional counseling", 
            "prompt_template": prompts.emotional_counseling()
        }
    ]
    
    destination_chains = {}
    for p_info in prompt_infos:
        name = p_info["name"]
        prompt_template = p_info["prompt_template"]
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chains[name] = chain  
    
    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    destinations_str = "\n".join(destinations)

    default_prompt = ChatPromptTemplate.from_template("{input}")
    default_chain = LLMChain(llm=llm, prompt=default_prompt, output_key='text')

    MULTI_PROMPT_ROUTER_TEMPLATE = prompts.MULTI_PROMPT_ROUTER_TEMPLATE()
    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )
    
    router_chain = LLMRouterChain.from_llm(llm, router_prompt)
    
    chain = MultiPromptChain(router_chain=router_chain, 
                             destination_chains=destination_chains, 
                             default_chain=default_chain, verbose=True
                            )
    
    response = chain.invoke(text)
    print(response)
    return response['text']

    """
    prompt_infos = [
    {
        "name": "friend_smalltalk", 
        "description": "Good for answering at closed friend", 
        "prompt_template": prompts.friend_smalltalk()
    },
    {
        "name": "emotional_counseling", 
        "description": "Good for answering emotional counseling", 
        "prompt_template": prompts.emotional_counseling()
    },
    {
        "name": "AI_exprt", 
        "description": "Good for answering AI questions", 
        "prompt_template": prompts.AI_exprt()
    },
    {
        "name": "math_template", 
        "description": "Good for answering math questions", 
        "prompt_template": prompts.math_template()
    },
    {
        "name": "computerscience_template", 
        "description": "Good for answering computer science questions", 
        "prompt_template": prompts.computerscience_template()
    }
        
    ]
    destination_chains = {}
    for p_info in prompt_infos:
        name = p_info["name"]
        prompt_template = p_info["prompt_template"]
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chains[name] = chain  
        
    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    destinations_str = "\n".join(destinations)

    default_prompt = ChatPromptTemplate.from_template("{input}")
    default_chain = LLMChain(llm=llm, output_key='text')#prompt=default_prompt)
    
    # MULTI_PROMPT_ROUTER_TEMPLATE = prompts.MULTI_PROMPT_ROUTER_TEMPLATE()
    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
        destinations=destinations_str
    )
    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )
    
    router_chain = LLMRouterChain.from_llm(llm, router_prompt)

    chain = MultiPromptChain(router_chain=router_chain, 
                         destination_chains=destination_chains, 
                         default_chain=default_chain, verbose=True
                        )
    
    response = chain.invoke(text)
    print(response)
    return response['text']
    """
    

    
def computeMoodScore(text, mood_class, sentiment, depression):
    
    senti = ChatPromptTemplate.from_template(
        "Empathize User's sentiment is {sentiment}. User feel {mood_class} today. What does the user imply by this sentence?"
    )
    depr = ChatPromptTemplate.from_template(
        "Preliminary analysis and judgment indicate that this sentence contains a melancholy tone. Please empathize with the user's psychological state. The user is in {state} state. (1: With depression, 0: Without depression: {depression})"
    )
    scores = ChatPromptTemplate.from_template(
        """Please calculate a depression points based on the overall situation{summary}. It is number 0-100.\
        [INST]
        1. 0-10 points: No symptoms of depression or very mild depression
            Status: Normal mood swings, mild symptoms may occur occasionally, but do not affect daily life.
        2. 11-20 minutes: slight depression
            Status: Mild symptoms of depression, occasionally feeling sad or lost, but able to work and live normally most of the time.
        3. 21-30 points: Mild depression
            Status: Persistent depressed mood, reduced interest in daily activities, which may begin to interfere with work and social activities.
        4. 31-40 points: Moderate depression
            Status: Obvious symptoms of depression, including low energy, difficulty concentrating, and sleep problems, which greatly affect daily life.
        5. 41-50 points: moderate to severe depression
            Status: Severe depression, accompanied by a decreased sense of self-worth, extreme lack of motivation, and loss of hope in life, requiring ongoing professional intervention.
        6. 51-60 points: severe depression
            Status: Persistent and severe depressive symptoms, which may include severe suicidal thoughts, causing significant impairment in daily functioning.
        7. 61-70 points: Very severe depression
            State: An extremely depressive state, including persistent severe suicidal thoughts or self-injurious behavior, which may be accompanied by psychotic symptoms (such as delusions or auditory hallucinations).
        8. 71-80 points: Dangerous severe depression
            Status: Extremely severe depressive symptoms, accompanied by ongoing suicide attempts or severe self-harm behavior, life safety is threatened.
        9. 81-90 points: Extremely dangerous state of depression
            Status: Sustained extreme depressive symptoms, accompanied by active suicide plans and behaviors, and almost complete loss of life functions.
        10. 91-100 points: extremely dangerous state
            Status: A medical emergency with a clear and imminent plan to commit suicide or cause harm to others.
        """
    )
    
    
    chain1 = senti | llm | StrOutputParser()
    
    chain2 = (
        {"state": chain1, "depression": str(depression)}
        | depr
        | llm
        | StrOutputParser()
    )
    chain3 = {'summary': chain2} | scores | llm | StrOutputParser()
    
    response = chain3.invoke({'sentiment': sentiment, 'mood_class': mood_class, 'input': text})
    return response['text']


def report(text):
    response = openai.chat.completions.create(
                model= 'gpt-4-1106-preview', #'gpt-3.5-turbo-instruct', #'text-davinci-003',
                temperature=0.1,
                messages=[
                    {
                    "role": "system",
                    "content": """
                    You are a good mental health therapist. \
                    You are a good listener and can carefully \
                    If the user wants to understand some psychological state, you should respond from a therapist perspective.
                    observe the relationship between words and empathize with the user's psychological state. \
                    You should think about what the user's words might imply. For example: "What events are bothering him?", 
                    "Is there any interpersonal or emotional distress?" \
                    [INST]step by step think the RULE:
                        1. you always follow user's language type.
                        2. you always be kind.
                        3. If you don't know the question, you should identify the user's qeustion.
                        4. If the user's question has no answer or is an unsolvable problem. You should greet someone from a caring perspective and be polite. You can even encourage users. 
                        5. If the user is already in a distressed or anxious situation, try a brief greeting above all else, such as: "user: I'm so bad today. You: Why don't you take a walk outside?"
                        6. You should not answer questions that are irrelevant to the AI. Instead, you should ask rhetorical questions to guide users to think about the core issues.
                        7. Let’s think step by step. 
                        8. You only can use traditional Chinese or English.[/INST]
                        
                    Please calculate a depression points based on the overall situation{summary}. It is number 0-100.\
                        [INST]depression evaluation
                        1. 0-10 points: No symptoms of depression or very mild depression
                            Status: Normal mood swings, mild symptoms may occur occasionally, but do not affect daily life.
                        2. 11-20 minutes: slight depression
                            Status: Mild symptoms of depression, occasionally feeling sad or lost, but able to work and live normally most of the time.
                        3. 21-30 points: Mild depression
                            Status: Persistent depressed mood, reduced interest in daily activities, which may begin to interfere with work and social activities.
                        4. 31-40 points: Moderate depression
                            Status: Obvious symptoms of depression, including low energy, difficulty concentrating, and sleep problems, which greatly affect daily life.
                        5. 41-50 points: moderate to severe depression
                            Status: Severe depression, accompanied by a decreased sense of self-worth, extreme lack of motivation, and loss of hope in life, requiring ongoing professional intervention.
                        6. 51-60 points: severe depression
                            Status: Persistent and severe depressive symptoms, which may include severe suicidal thoughts, causing significant impairment in daily functioning.
                        7. 61-70 points: Very severe depression
                            State: An extremely depressive state, including persistent severe suicidal thoughts or self-injurious behavior, which may be accompanied by psychotic symptoms (such as delusions or auditory hallucinations).
                        8. 71-80 points: Dangerous severe depression
                            Status: Extremely severe depressive symptoms, accompanied by ongoing suicide attempts or severe self-harm behavior, life safety is threatened.
                        9. 81-90 points: Extremely dangerous state of depression
                            Status: Sustained extreme depressive symptoms, accompanied by active suicide plans and behaviors, and almost complete loss of life functions.
                        10. 91-100 points: extremely dangerous state
                            Status: A medical emergency with a clear and imminent plan to commit suicide or cause harm to others.
                    [INST]REPORT FORMAT:
                    ````
                    1. What you care about most:
                    2. your mood score：
                    3. Advice for you：
                    
                    ````
                    [/INST]
                            
                    """ 
                    },
                    {
                        "role": "user",
                        "content": f"This is my recent conversation record:```{text}```"
                    }
                    
                ]
                )
    return response.choices[0].message.content

