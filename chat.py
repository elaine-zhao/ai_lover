from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

chat = ChatOpenAI()
print(chat([HumanMessage(content="Translate this sentence from English to French: I love programming.")]))