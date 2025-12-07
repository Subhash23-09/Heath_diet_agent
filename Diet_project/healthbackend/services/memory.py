from langchain.memory import ConversationBufferMemory

_shared_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

def get_shared_memory() -> ConversationBufferMemory:
    return _shared_memory

def reset_memory():
    _shared_memory.clear()
