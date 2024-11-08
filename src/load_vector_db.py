import os
import sys
import shutil
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import hashlib
from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

def initialize_vector_db(db_path):

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    vector_store = Chroma(
        collection_name="NOV-Product",
        embedding_function=embeddings,
        persist_directory=db_path,  # Where to save data locally, remove if not necessary
    )

    return vector_store


def initialize_text_splitters():

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter


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


def get_metadata(document_hash, file_name, file_path, document_type, url):
    return {
        "document_hash": document_hash,
        "file_name": file_name,
        "file_path": file_path,
        "document_type": document_type,
        "url": url
    }


def create_docs(document, metadata):

    docs = text_splitter.create_documents([document], [metadata])
    return docs


def add_docs_db(docs):
    vector_store.add_documents(documents=docs)
    print(f"File '{file_name}' has been successfully loaded into the vector database.")
    return


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
    return dest_file, file_name


if __name__ == "__main__":
    document_types = ['brochures', 'case_study', 'catalog', 'faq', 'flyers', 'handbook', 'policy', 'publication', 'reference_guide', 'spec_and_data_sheet', 'technical_paper', 'white_paper', 'other']
    # Check if file path is passed as an argument
    if len(sys.argv) < 4:
        print("Usage: python ./src/load_vector_db.py <path_to_file> <url_to_file> <document type>")
        print("<path_to_file>: The local path to the document you want to add.")
        print("<url_to_file>: The URL to the document you want to add.")
        print("Document Type must be: " + " ".join(str(i) + ". " + document_types[i] for i in range(len(document_types ))))
    else:
        file_path = sys.argv[1]
        file_url = sys.argv[2]
        document_folder = sys.argv[3]
        if document_folder in document_types:
            file_name = os.path.basename(file_path)
            db_path = os.path.join(os.getcwd(), "chroma_langchain_db")
            vector_store = initialize_vector_db(db_path)
            text_splitter = initialize_text_splitters()
            document_content = extract_pdf_text(file_path)
            document_hash = get_hash(document_content)
            hash_flag = check_hash(document_hash)
            if hash_flag:
                print("Document is already stored in database.")
            else:
                metadata = get_metadata(
                    document_hash, file_name, file_path, document_folder, file_url
                )
                docs = create_docs(document_content, metadata)
                add_docs_db(docs)
                copy_document(file_path, document_folder)
        else:
            print("Document Type must be: " + " ".join(str(i) + ". " + document_types[i] for i in range(len(document_types ))))
