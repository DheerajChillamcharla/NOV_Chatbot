from context_retriever import context_retriever
from langchain_core.runnables import RunnablePassthrough
from prompt import prompt_template
from llm import llm
from langchain_core.output_parsers import StrOutputParser

rag_chain = (
    {
        "query": RunnablePassthrough(),
        "formatted_context": lambda x: context_retriever(x),
    }
    | prompt_template()
    | llm()
    | StrOutputParser()
)

print(rag_chain.invoke("Explain capacities of Tool OD: 1 5/8 in."))
