from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os 
import sqlite3
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
chat = ChatOpenAI(model="gpt-3.5-turbo-1106",api_key=os.environ.get("OPENAI_API_KEY"))


# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful assistant. Answer all questions to the best of your ability.",
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

# chain = prompt | chat 

# chain.invoke(
#     {
#         "messages": [
#             HumanMessage(
#                 content="Translate this sentence from English to French: I love programming."
#             ),
#             AIMessage(content="J'adore la programmation."),
#             HumanMessage(content="What did you just say?"),
#         ],
#     }
# )

# # AIMessage(content='I said "J\'adore la programmation," which means "I love programming" in French.')


prompt = ChatPromptTemplate.from_template("tell me a short story about {topic}")
model = ChatOpenAI(model="gpt-4", api_key=os.environ.get("OPENAI_API_KEY"))
output_parser = StrOutputParser()

chain = prompt | model | output_parser

print(chain.invoke({"topic": "startup"}))


