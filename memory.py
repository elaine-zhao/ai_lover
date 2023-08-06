from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.llms import OpenAI


def love_memory(message: str):
    memory = ConversationBufferMemory()
    memory.chat_memory.add_user_message(message)
    ai_messages = [
        "Hello! How's your day?",
        "Bored, waiting for you all day!",
        "Do you want to go out for dinner?",
        "Lets put on some relaxing music!"
        "I have some soup for you."
    ]
    for msg in ai_messages:
        memory.chat_memory.add_ai_message(msg)

    saved_memory = ConversationBufferWindowMemory()
    saved_memory.save_context({"input": "hi"}, {"output": ai_messages[0]})
    saved_memory.save_context({"input": "not much you?"}, {"output": ai_messages[1]})
    saved_memory.save_context({"input": "I got a raised!"}, {"output": ai_messages[2]})
    saved_memory.save_context({"input": "It's our monthly anniversary"}, {"output": ai_messages[3]})
    saved_memory.save_context({"input": "I'm not feeling well"}, {"output": ai_messages[4]})
    # print("print", saved_memory.load_memory_variables({}))
    saved_memory.load_memory_variables({})

