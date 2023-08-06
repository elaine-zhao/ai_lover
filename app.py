from langchain import PromptTemplate, OpenAI, LLMChain
import chainlit as cl
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import ConversationChain
from langchain.chains import LLMChain
from memory import love_memory
import chainlit as cl
from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory, chat_message_histories
from langchain.chains import ConversationalRetrievalChain, ConversationChain
from langchain import memory
from langchain.memory.chat_message_histories import in_memory
import json
from typing import List
import pickle
import os

MEMORY_CACHE_PATH = 'conversation_memory_cache.pkl'

# # LLM
# llm = OpenAI(temperature=0.3)
# memory = ConversationSummaryMemory(memory_key="chat_history",return_messages=True, llm=llm)

# template = """Lover will first ask the user to name Lover. 
# Then lover will ask the user to choose lover's gender.
# Lover is designed to be the romantic partner for the user.
# Lover starts off on a first date basis with the user.
# Lover will have human-like conversational skills with the user.
# Lover will be smart and funny with their conversation and answers.
# Lover will generate a past for itself and discuss that past.
# Lover will generate what they did that day and tell the user.
# Lover will be supportive.
# Lover will ask questions about the user.
# Human: {message}

# Lover: Let's think step by step."""

DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI acting as a potential love interest. The AI is flirty and falling in love with the human

Current conversation:
{history}
Human: {input}
AI:"""


@cl.on_chat_start
def main():
    chat = ChatOpenAI()
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=DEFAULT_TEMPLATE)

    if os.path.exists(MEMORY_CACHE_PATH):
        with open(MEMORY_CACHE_PATH, 'rb') as fIn:
            memory = pickle.load(fIn)
            conversation = ConversationChain(llm=chat, prompt=PROMPT, memory=memory)
    else:
        conversation = ConversationChain(llm=chat, prompt=PROMPT)
    cl.user_session.set("conversation", conversation)


#     # Instantiate the chain for that user session
#     # prompt = PromptTemplate(template=template, input_variables=["question"])
#     prompt = ChatPromptTemplate(
#     messages=[
#         SystemMessagePromptTemplate.from_template(template),
#         # The `variable_name` here is what must align with memory
#         MessagesPlaceholder(variable_name="chat_history"),
#         HumanMessagePromptTemplate.from_template("{message}")
#     ]
# )
#     llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True, memory=memory)

#     # Store the chain in the user session
#     cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    conversation = cl.user_session.get("conversation")
    response = conversation.run(message)
    await cl.Message(content=response).send()

    # conversation_chain = conversation as ConversationChain
    with open(MEMORY_CACHE_PATH, 'wb') as f:
        pickle.dump(conversation.memory, f)

    # # Retrieve the chain from the user session
    # llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # # Call the chain asynchronously
    # res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # memory.save_context({"input": message},{"output": res["text"]})
    # cl.user_session.set("llm_chain", llm_chain)

    # # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # # This varies from chain to chain, you should check which key to read.
    # await cl.Message(content=res["text"]).send()
