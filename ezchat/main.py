import os   
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryMemory, FileChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    verbose=True,
)

memory = ConversationSummaryMemory(
    #chat_memory=FileChatMessageHistory(file_path="chat_memory.json",max_messages=100),
    memory_key="messages",
    return_messages=True,
    llm=chat,
)

prompt = ChatPromptTemplate(
    input_variables=["content"],
    messages=[
        MessagesPlaceholder(memory_key="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,  
    verbose=True,
)


while True:
    content = input(">>> ")
    result = chain({"content": content})
    print(result['text'])