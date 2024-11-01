import os
import sys
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import hashlib

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


def extract_pdf_text(pdf_path):
    """
    Extract text from all pages of a PDF file.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        dict: Dictionary with page numbers as keys and extracted text as values
        str: Complete text from all pages combined
    """

    # Create PDF reader object
    reader = PdfReader(pdf_path)

    # Dictionary to store page-wise text
    pages_text = {}

    # Complete text from all pages
    full_text = ""

    # Extract text from each page
    for page_num in range(len(reader.pages)):
        # Get the page object
        page = reader.pages[page_num]

        # Extract text from page
        text = page.extract_text()

        # Store in dictionary (0-based index)
        pages_text[page_num] = text

        # Add to full text with page separator
        full_text += f"\n\n{text}"

    return full_text


def get_hash(document):
    """Compute SHA-256 hash of document content."""
    return hashlib.sha256(document.encode()).hexdigest()


def check_hash(document_hash):

    results = vector_store.get(where={"document_hash": document_hash})
    if len(results["ids"]) == 0:
        return False
    else:
        return True


def copy_document(document_path, document_folder):
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

    load_document(dest_file, file_name)
    return dest_file, file_name


def load_document(document_path, file_name):
    loader = PyPDFLoader(document_path)

    docs = loader.load_and_split(text_splitter)
    vector_store.add_documents(documents=docs)
    print(f"File '{file_name}' has been successfully loaded into the vector database.")


if __name__ == "__main__":

    # Check if file path is passed as an argument
    if len(sys.argv) < 3:
        print("Usage: python store_file.py <path_to_file> <document type")
        print("Document Types : 1.catalog 2.other")
    else:
        file_path = sys.argv[1]
        document_folder = sys.argv[2]

        document_content = extract_pdf_text(file_path)
        document_hash = get_hash(document_content)
        hash_flag = check_hash(document_hash)
        if hash_flag:
            print("Document is already stored in database'.")
        else:
            pass
            # dest_file_path, file_name = copy_document(file_path, document_folder)
