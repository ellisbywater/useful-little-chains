from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from handlers.chat_model_start_handlers import ChatModelStartHandler

from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_table_tool, write_report_tool

load_dotenv()

handler = ChatModelStartHandler()
chat = ChatOpenAI(
    callbacks=[handler],
)
tables = list_tables()
print(tables)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite Database \n",
            "The database has the following tables: \n",
            f"{tables} \n",
            "Do not make assumptions about the schema of the tables \n",
            "Instead, use the describe_tables tool to get the schema for a table \n",
            )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

memory = ConversationBufferMemory()
tools = [run_query_tool, describe_table_tool, write_report_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
)

agent_executor("How many users are in the database?")