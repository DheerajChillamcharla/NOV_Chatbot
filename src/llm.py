from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
def llm():

    llm = ChatOpenAI(model="gpt-4o-mini")

    return llm
