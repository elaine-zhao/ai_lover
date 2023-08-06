from langchain import PromptTemplate, OpenAI, LLMChain
from conversation import process_response
import chainlit as cl
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from memory import love_memory
import chainlit as cl
from langchain.memory import ConversationSummaryMemory


# LLM
llm = OpenAI(temperature=0.3)
memory = ConversationSummaryMemory(memory_key="chat_history",return_messages=True, llm=llm)

template = """Lover will first ask the user to name Lover. 
Then lover will ask the user to choose lover's gender.
Lover is designed to be the romantic partner for the user.
Lover starts off on a first date basis with the user.
Lover will have human-like conversational skills with the user.
Lover will be smart and funny with their conversation and answers.
Lover will generate a past for itself and discuss that past.
Lover will generate what they did that day and tell the user.
Lover will be supportive.
Lover will ask questions about the user.
Human: {message}

Lover: Let's think step by step."""


@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    # prompt = PromptTemplate(template=template, input_variables=["question"])
    prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(template),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{message}")
    ]
)
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True, memory=memory)

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    memory.save_context({"input": message},{"output": res["text"]})
    cl.user_session.set("llm_chain", llm_chain)

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()
