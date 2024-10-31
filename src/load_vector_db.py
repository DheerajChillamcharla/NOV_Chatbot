import os
import sys
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from langchain import hub


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = Chroma(
    collection_name="NOV-Product",
    embedding_function=embeddings,
    persist_directory="../chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)


def document_loader(document_path, document_folder):
    # Check if the file exists
    if not os.path.isfile(document_path):
        print(f"Error: The file '{document_path}' does not exist.")
        return

    # Get the file name from the provided path
    file_name = os.path.basename(document_path)

    # Define the destination path
    dest_path = os.path.join(os.getcwd(), "data", document_folder)
    dest_file = os.path.join(dest_path, file_name)
    # Copy the file to the project folder
    shutil.copy(file_path, dest_path)
    print(f"File '{file_name}' has been successfully stored in '{document_folder}'.")

    load_document_db(dest_file, file_name)


def load_document_db(document_path, file_name):
    loader = PyPDFLoader(document_path)

    docs = loader.load_and_split(text_splitter)
    print(f"File '{file_name}' has been successfully loaded into the vector database.")



if __name__ == "__main__":

    # Check if file path is passed as an argument
    if len(sys.argv) < 3:
        print("Usage: python store_file.py <path_to_file> <document type")
        print("Document Types : 1.catalog 2.other")
    else:
        file_path = sys.argv[1]
        document_folder = sys.argv[2]
        document_loader(file_path, document_folder)
