import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import argparse

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--task", type=str, default="Return the sum of two numbers")
parser.add_argument("--language", type=str, default="python")
args = parser.parse_args()



llm = OpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

code_prompt = PromptTemplate(
    template="Write a {language} function that will {task}.",
    input_variables=["language", "task"],
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt
)

result = code_chain({
    "language": args.language,
    "task": args.task
})

print(result['text'])