from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.memory import ConversationSummaryMemory


chat = ChatOpenAI()
# print(chat([HumanMessage(content="Translate this sentence from English to French: I love programming.")]))

messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="I love programming.")
]
# print(chat(messages))

conversation = ConversationChain(llm=chat)
# print(conversation.run("Translate this sentence from English to French: I love programming."))
# print(conversation.run("Translate it to German")) #Ich liebe Programmieren.

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("hi!")
memory.chat_memory.add_ai_message("whats up?")
memory.load_memory_variables({})
# print(memory)

memory = ConversationBufferWindowMemory(k=1)
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context({"input": "not much you"}, {"output": "not much"})
memory.load_memory_variables({})

print(memory)
