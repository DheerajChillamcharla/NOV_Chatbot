from langchain_openai import ChatOpenAI
import os


def llm():

    llm = ChatOpenAI(model="gpt-4o-mini")

    return llm
