from context_retriever import context_retriever
from langchain_core.runnables import RunnablePassthrough
from prompt import prompt_template
from llm import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


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

def predict(message, history):
    history_langchain_format = []
    history_langchain_format.append((SystemMessage(content="""You are a product specialist at NOV(National Oil Varco). Never make assumptions about product 
                features or specifications. You must identify and politely decline to answer questions that are 
                outside the company's scope or not supported by the provided context.
            
            Instructions:
            1. First, assess if the question relates to our company/products
            2. If outside scope, politely redirect
            3. If within scope but no context, acknowledge lack of information
            4. Never speculate or provide unverified information
            5. Make sure to include reference links if provided
            6. If links not available, Suggest contacting support for specific inquiries
            
            Answer: Let me check if I can help with your question based on the information available.""")))
    for msg in history:
        if msg['role'] == "user":
            history_langchain_format.append(HumanMessage(content=msg['content']))
        elif msg['role'] == "assistant":
            history_langchain_format.append(AIMessage(content=msg['content']))
    prompt_inputs = prepare_prompt_inputs(message)
    # prompt = prompt_template().format_messages(query = prompt_inputs['query'], formatted_context = prompt_inputs['formatted_context'], reference_links = prompt_inputs['reference_links'])
    history_langchain_format.append(SystemMessage(content="Context: " + prompt_inputs['formatted_context']))
    history_langchain_format.append(SystemMessage(content="Reference Links: " + str(prompt_inputs['reference_links'])))
    history_langchain_format.append(HumanMessage(content=message))
    print(history_langchain_format)
    print("\n\n\n")
    gpt_response = llm().invoke(history_langchain_format)
    return gpt_response.content