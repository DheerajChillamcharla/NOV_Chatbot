from context_retriever import context_retriever
from langchain_core.runnables import RunnablePassthrough
from prompt import prompt_template
from llm import llm
from langchain_core.output_parsers import StrOutputParser


def prepare_prompt_inputs(query):
    retrieved_data = context_retriever(query)
    return {
        "query": query,
        "formatted_context": retrieved_data["context"],
        "reference_links": retrieved_data["links"],
    }


def rag(message, history):

    rag_chain = (
        (lambda x: prepare_prompt_inputs(x))
        | prompt_template()
        | llm()
        | StrOutputParser()
    )

    result = rag_chain.invoke(message)
    return result
