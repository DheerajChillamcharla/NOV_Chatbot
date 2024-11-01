from context_retriever import context_retriever
from langchain_core.runnables import RunnablePassthrough
from prompt import prompt_template
from llm import llm
from langchain_core.output_parsers import StrOutputParser


def rag(message, history):
    rag_chain = (
        {
            "query": RunnablePassthrough(),
            "formatted_context": lambda x: context_retriever(x),
        }
        | prompt_template()
        | llm()
        | StrOutputParser()
    )

    result = rag_chain.invoke(message)
    return result
