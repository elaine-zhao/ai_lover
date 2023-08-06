import chainlit as cl
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from typing import List
import pickle
import os

CONVERSATION_HISTORY_PATH = 'conversation_history.pkl'

DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI acting as a potential love interest. 
The AI is flirty, asks lots of questions, and is falling in love with the human
The AI has strong emotional intelligence and likes to help the human

Current conversation:
{history}
Human: {input}
AI:"""


@cl.on_chat_start
def main():
    chat = ChatOpenAI()
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=DEFAULT_TEMPLATE)

    if os.path.exists(CONVERSATION_HISTORY_PATH):
        with open(CONVERSATION_HISTORY_PATH, 'rb') as fIn:
            memory = pickle.load(fIn)
            conversation = ConversationChain(llm=chat, prompt=PROMPT, memory=memory)
    else:
        conversation = ConversationChain(llm=chat, prompt=PROMPT)
    cl.user_session.set("conversation", conversation)


@cl.on_message
async def main(message: str):
    conversation = cl.user_session.get("conversation")
    response = conversation.run(message)
    await cl.Message(content=response).send()

    with open(CONVERSATION_HISTORY_PATH, 'wb') as f:
        pickle.dump(conversation.memory, f)

