from load_vector_db import initialize_vector_db
import os


def context_retriever(query):
    # Retrieve and generate using the relevant snippets of the blog.
    db_path = os.path.join(os.getcwd(), "../chroma_langchain_db")
    vector_store = initialize_vector_db(db_path)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,
            "fetch_k": 6,
            "lambda_mult": 0.75,
            "score_threshold": 0.75,
        },
    )
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    url = [doc.metadata.get("url", "No URL found") for doc in docs]

    return {"context": context, "links": url}
