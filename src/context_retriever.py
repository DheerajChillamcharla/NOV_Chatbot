from load_vector_db import embeddings, vector_store


def context_retriever(query):
    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    return context