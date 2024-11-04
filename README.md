# RAG Chat Bot for NOV

## Introduction 

This project introduces an innovative Retrieval-Augmented Generation (RAG) chatbot designed to streamline access to NOV’s extensive product documentation. Leveraging advanced OpenAI models via API integration and a robust Chroma DB vector database, Langchain framework, the chatbot delivers accurate and context-rich answers to user queries about technical specifications, use cases, brochures, and more. By combining powerful language generation with efficient document retrieval, this solution addresses the challenge of navigating vast information repositories, ensuring users receive precise and relevant information quickly and effortlessly. This approach not only enhances user experience but also empowers efficient decision-making through easy access to critical product details

## Features

- **Product-Focused Q&A**: Purpose-built to answer queries about NOV’s products, covering everything from technical specifications and use cases to in-depth product descriptions sourced directly from the document library.
- **OpenAI API Integration**: Utilizes state-of-the-art OpenAI models to generate precise, context-aware responses, ensuring a high-quality user experience.
- **Efficient Document Retrieval**: Implements advanced techniques to extract and present relevant content from NOV’s brochures, case studies, catalogs, and more, minimizing search time and effort.
- **Dynamic Knowledge Base**: Continuously updated to reflect the latest information from NOV, ensuring the chatbot stays current and reliable.
- **Robust Error Handling**: Gracefully manages ambiguous queries by offering suggestions or requests for clarification, enhancing overall usability.
- **Customizable and Scalable**: Built for future enhancements, making it easy to incorporate new features or expand the knowledge base as needed.
- **Secure and Local Data Storage**: Uses Chroma DB for fast, AI-native data storage while prioritizing data security and privacy.

## Access to Chatbot

This chatbot is hosted on Hugging Face Spaces and can be accessed through the following link:

[Access the NOV Chatbot](https://huggingface.co/spaces/dheeraj-ch/NOV-chatbot)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Access to Chatbot](#access-to-chatbot)
- [Retrieval](#retrieval)
  - [Overview of Data](#overview-of-data)
  - [Data Storage and Embeddings](#data-storage-and-embeddings)
    - [1. Vector Database](#1-vector-database)
    - [2. Embeddings](#2-embeddings)
    - [3. Techniques for Data Integrity](#3-techniques-for-data-integrity)
  - [Context Retrieval](#context-retrieval)
- [Augmenting](#augmenting)
- [Generation](#generation)
- [Benfits of RAG](#benfits-of-rag)
- [Gradio UI](#gradio-ui)
- [User Installation Guide](#user-installation-guide)
- [Adding New Documents to the Knowledge Base](#adding-new-documents-to-the-knowledge-base)
- [Troubleshooting](#troubleshooting)
- [Future Scope](#future-scope)
- [References and Citations](#references-and-citations)
- [Contact](#contact)

## Retrieval 
### Overview of Data

The data used for this project is scraped from NOV's extensive document library. The resources cover a wide range of document types, each containing critical information about NOV’s products and operations. The categories of documents included in the knowledge base are:

- **Brochures**
- **Case Studies**
- **Catalogs**
- **FAQs**
- **Flyers**
- **Handbooks**
- **Policies**
- **Publications**
- **Reference Guides**
- **Spec and Data Sheets**
- **Technical Papers**
- **Technical Summaries**
- **White Papers**

Additionally, supplementary information from the official NOV website and the NOV Wikipedia page is incorporated to provide a more robust and contextually relevant knowledge base. 

### Data Storage and Embeddings

To efficiently manage and retrieve the information from NOV's extensive document library, the project uses a combination of a vector database, embeddings, and data integrity techniques. This approach ensures that the chatbot delivers accurate and contextually relevant responses.

### 1. Vector Database
**Chroma DB** is used as the vector database for this project. Chroma DB is an open-source, AI-native, and locally hosted database solution, making it an excellent choice for the following reasons:
- **Efficiency**: It provides high-speed storage and retrieval of embeddings, which is crucial for real-time responses.
- **Scalability**: As an AI-native database, it is optimized to handle large volumes of vector data efficiently.
- **Local and Secure**: Being locally hosted, Chroma DB ensures data privacy and security, making it suitable for projects dealing with sensitive information.

### 2. Embeddings
The model **"sentence-transformers/all-mpnet-base-v2"** from Hugging Face is used for generating embeddings. This model is a suitable choice because:
- **High Performance**: It offers state-of-the-art performance on various sentence similarity and retrieval tasks.
- **Semantic Understanding**: The model excels at capturing semantic meaning from text, ensuring that the embeddings reflect the context and nuances of the content.
- **Wide Adoption**: Its widespread use and community support make it a reliable and well-documented option for embedding tasks.

### 3. Techniques for Data Integrity
To maintain the integrity of the database and ensure the quality of the data processed, several techniques are implemented:

- **Hashing for Integrity**: 
  - **Purpose of Hashing**: Hashing is used to create a unique fingerprint for each document, ensuring that duplicates are not introduced into the database. This is crucial for maintaining data integrity and optimizing storage space.
  - **How It Works**: When a document is loaded, a hash (e.g., using SHA-256) is generated based on the document's content. This hash is then compared with the existing hashes stored in the database:
    - **Duplicate Check**: If a matching hash is found, the document is identified as already processed, and loading is skipped. This prevents duplicate data from being stored and ensures the chatbot does not provide redundant or conflicting information.
    - **Chunk-Level Tracking**: The hash is stored alongside each chunk. By associating the hash with each chunk, the system can effectively track and manage document chunks, ensuring that chunks belonging to the same document are linked and managed cohesively.
  - **Avoiding Redundant Processing**: The use of hashing also optimizes the workflow by avoiding reprocessing or re-embedding content that has not changed, saving computational resources and maintaining a streamlined database.

- **Document Chunking**: Documents are divided into chunks of size 1000 tokens with an overlap of 200 tokens. This chunking strategy ensures that relevant context is preserved across chunks, enhancing the quality of retrieval and response generation.

- **Metadata Storage**: Important metadata is stored for each chunk, including:
  - `document_hash`: The unique hash for the document.
  - `file_name`: The name of the original file.
  - `file_path`: The path to the file in the data source.
  - `document_type`: The category or type of the document (e.g., brochure, case study).
  - `url`: The original URL from which the document was scraped.
  
  This metadata provides critical information for tracking and managing document chunks effectively.
  
- **PDF Extraction**: **PyPDF** is used to extract text information from PDFs, ensuring reliable and efficient data extraction.
  
- **Document Splitting**: The **Recursive Text Splitter** from LangChain is used to split documents into manageable chunks. This method ensures that the text is divided efficiently while preserving meaningful context.

### Context Retrieval

The context retrieval process is designed to fetch the most relevant snippets of information from the vector database to provide context along with query to large language model. This ensures that the chatbot provides precise and comprehensive answers to user queries. Here’s how the retrieval process is structured:

### How Context Retrieval Works

1. **Maximal Marginal Relevance (MMR) Search**:
   - The retriever uses **MMR**, a search technique that balances relevance and diversity in the retrieved results.
   - **Relevance**: Ensures that the returned snippets closely match the user’s query, helping the chatbot provide accurate responses.
   - **Diversity**: Incorporates varied snippets to avoid redundant information, giving the chatbot a richer context for generating answers.

2. **Parameter Tuning for Optimal Results**:
   - **k**: Controls the number of top-ranked snippets to be included in the response context. This ensures that only the most relevant information is used.
   - **fetch_k**: Specifies how many documents to retrieve initially before ranking, providing a larger pool of snippets for selection.
   - **lambda_mult**: A parameter that controls the balance between relevance and diversity in the MMR algorithm, fine-tuned to ensure high-quality responses.
   - **score_threshold**: Filters out less relevant documents by setting a minimum relevance score, ensuring that only meaningful content contributes to the context.

3. **Context Assembly**:
   - Once the top snippets are retrieved, they are combined into a single context block that the chatbot uses to generate responses.
   - The context is built by joining the content of each retrieved document, creating a cohesive and informative answer.

4. **Metadata for Traceability**:
   - Along with the context, the URLs and metadata for each document are retained, providing users with references to the original sources of information. This enhances traceability and offers a way to verify or further explore the information provided.

This retrieval process ensures that the chatbot draws from a well-curated and diverse set of snippets, providing users with reliable and contextually rich answers.

## Augmenting

The augmenting process is a crucial step where the user query is enhanced with additional context and reference links to maximize the quality of the generated response. This is achieved through careful prompt engineering and the integration of relevant information.

### Prompt Engineering
Prompt engineering involves crafting efficient and effective prompts for the language model to ensure accurate and meaningful responses. This process includes experimenting with various prompt formats and testing their performance to select the most suitable one.

- **Purpose**: The main objective of prompt engineering is to guide the model to generate precise and contextually relevant answers by structuring the prompt effectively.

### How It Works
1. **Context Augmentation**: The user query is enriched with the retrieved context from the vector database. This ensures the model has sufficient information to generate an accurate and informative response.
2. **Reference Links**: The URLs associated with the retrieved documents are included in the prompt to provide traceability and reference points for the generated information.
3. **Prompt Structure**: The final prompt fed to the model is a well-structured combination of:
     - The original user query
     - The augmented context
     - The reference links
4. **Specific Instructions**: The prompt includes clear instructions to the model to:
    - Avoid making assumptions or speculating about the information.
    - Provide only verified and factual content related to NOV and its products.
   
This structured prompt enhances the model's understanding and ensures the generated answer is both relevant and well-informed.

This well-designed augmenting process is key to delivering high-quality, contextually rich responses from the RAG chatbot.

## Generation

The generation process is responsible for transforming the augmented user query and context into a meaningful and accurate response. This is achieved through the use of a powerful language model and a well-structured RAG (Retrieval-Augmented Generation) chain.

### 1. Large Language Model (LLM)
The project uses OpenAI's large language models (LLMs) accessed via API. These models are a suitable choice for several reasons:

- **State-of-the-Art Performance**: OpenAI's models are among the most advanced in the field, known for their exceptional ability to understand and generate human-like text. This ensures that responses are natural, coherent, and relevant.
- **Contextual Understanding**: The models excel at interpreting complex queries and generating responses that reflect the nuances of the provided context. This is especially important for a chatbot that needs to provide detailed, product-specific information.
- **Flexibility and Customization**: OpenAI's LLMs are highly adaptable, allowing for prompt customization and fine-tuning of responses to meet the specific needs of this project, such as focusing solely on NOV-related content.
- **API Integration**: Using the OpenAI API allows seamless integration into the project, making it easy to leverage the full power of these models while maintaining efficient communication and processing.

### 2. RAG Chain
The RAG (Retrieval-Augmented Generation) chain is a structured workflow that processes the input in a streamlined manner to produce a high-quality response. Here's how it works:

- **Pipeline Structure**: The RAG chain is set up like a pipeline, where each component works in sequence to transform the user query into a final response. This structured approach ensures that all steps—retrieval, augmentation, and generation—are seamlessly integrated.
- **Step-by-Step Process**:
  1. **Input**: The user query, along with the retrieved context and reference links, is fed into the chain.
  2. **Context and Prompt Handling**: The augmented information is structured into a well-crafted prompt, as described in the augmenting process.
  3. **LLM Processing**: The OpenAI LLM takes this prompt and generates a response. The LLM uses the provided context to ensure that the output is accurate, relevant, and aligned with the user’s query.
  4. **Output**: The generated response is then returned, ready for the user, complete with any reference links that were included in the prompt.

## Benfits of RAG 
  - **High Accuracy**: By combining Maximal Marginal Relevance (MMR) and optimized search parameters with a well-engineered RAG chain, the system delivers highly accurate and relevant responses.
  - **Broad Information Scope**: The diversity element in MMR allows the chatbot to consider a wide range of information, resulting in well-rounded and comprehensive answers.
  - **Contextual Relevance**: The RAG chain ensures that the language model has all the necessary context to generate informative and accurate responses, particularly tailored to NOV’s products and content.
  - **Traceable and Verifiable Information**: Including reference links in the responses makes the information more trustworthy and allows users to verify or further explore the sources.
  - **Focused Information**: Prompt engineering and strict instructions ensure that the model only discusses NOV-related content, keeping all answers relevant and aligned with the project's goals.
  - **Efficiency and Scalability**: The use of a locally hosted vector database and efficient retrieval algorithms, along with a pipeline approach in the RAG chain, makes the system scalable and capable of handling large datasets while reducing latency.
  - **Seamless Integration**: The OpenAI API integration enables a smooth and efficient generation process, ensuring high-quality responses without delays.
  - **Optimized User Experience**: By minimizing the need for repeated queries and ensuring efficient information access, the system enhances the overall user experience and provides timely, accurate answers.

This well-orchestrated generation process is key to delivering an exceptional user experience, leveraging the strengths of OpenAI's LLMs and the efficiency of the RAG chain structure.

## Gradio UI

**Gradio** is used for the front-end interface, providing a simple and interactive way for users to engage with the chatbot. It allows for quick and efficient setup with minimal code, making integration seamless. 

### How It’s Used
- **Ease of Use**: Gradio simplifies the creation of a web-based UI, requiring only a few lines of code.
- **Seamless Integration**: Connects effortlessly with the backend, ensuring smooth interactions from query to response.
- **Customizable**: Offers flexibility to tailor the interface to project needs while remaining user-friendly and visually appealing.
- **Rapid Deployment**: Easily deployable locally or on the cloud, making it ideal for testing and sharing.

Gradio’s simplicity and efficiency make it an excellent choice for building a clean, responsive UI with minimal development effort.

## Hugging Face Spaces

The project is deployed on **Hugging Face Spaces**, which provides an easy and efficient way to host applications with minimal setup. It supports frameworks like Gradio and offers free hosting, making it ideal for rapid prototyping and sharing. Additionally, being integrated into the Hugging Face ecosystem grants access to a large community and resources, while ensuring reliable performance and scalability for the chatbot.

## User Installation Guide

This guide will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.12
- Chrome Browser

### Steps to Install and Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/DheerajChillamcharla/NOV_Chatbot.git
```

### 2. Navigate to the Project Folder

```bash
cd NOV_Chatbot
```

### 3. Set Up a Virtual Environment Using virtualenv

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:
```bash
venv\Scripts\activate
```
For macOS/Linux:
```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Set OPENAI_API_KEY as an Environment Variable

For Windows:
```bash
set OPENAI_API_KEY=your-api-key
```
For macOS/Linux:
```bash
export OPENAI_API_KEY=your-api-key
```

### 7. Download Chromedriver

- Download the chromedrive that matches with the chrome version from https://developer.chrome.com/docs/chromedriver/downloads
- Move chromedriver.exe file to project folder

### 8. Run the Application

```bash
python ./src/app.py
```

### 9. Open the Application in Your Browser

Visit: http://127.0.0.1:7860

## Adding New Documents to the Knowledge Base

To keep the knowledge base updated with the latest documents, follow these steps to add a new document.

### Steps to Add a New Document

1. **Navigate to the Project Folder**
   ```bash
   cd your-repo-name
   ```

2. **Run the Document Loading Script**
   
   Use the following command to load a new document into the vector database:
   ```bash
   python ./src/load_vector_db.py <path_to_file> <url_to_file> <document_type>
   ```

   Parameters:
   - `<path_to_file>`: The local path to the document you want to add.
   - `<url_to_file>`: The URL where the document is hosted (if applicable), if url not available use " "
   - `<document_type>`: The type of document being added. Use one of the following predefined types:
     - Brochures, Case Studies, Catalogs, Certifications, FAQs, Flyers, Forms
     - Handbooks, Policies, Publications, Reference Guides, Spec and Data Sheets
     - Technical Papers, Technical Summaries, White Papers


## Troubleshooting

### 1. Build Error When Running `pip install chromadb`

If you encounter an error like the one shown below during setup:

```
Failed to build hnswlib ERROR: Could not build wheels for hnswlib, which is required to install pyproject.toml-based projects
```

Try these solutions recommended by the chromadb community:

### If you get the error: "clang: error: the clang compiler does not support '-march=native'"
- Set this environment variable:
  ```bash
  export HNSWLIB_NO_NATIVE=1
  ```

### If on Mac
- Install or update Xcode developer tools:
  ```bash
  xcode-select --install
  ```

### If on Windows
Try [these steps](https://github.com/chroma-core/chroma/issues/250#issuecomment-1540934224).

## Future Scope

Here are some potential enhancements and future improvements for the RAG chatbot project:

1. **Enhanced Knowledge Base Management**:
   - Add functionality to delete or update documents in the knowledge base.
   - Implement mechanisms to detect and handle duplicate or similar documents efficiently.

2. **Contextual Query Enhancement**:
   - Use large language models (LLMs) to dynamically enrich and refine user queries, ensuring better context matching when searching for relevant information in the database. This would improve the accuracy and relevance of the retrieved context.

3. **Advanced Conversational Capabilities**:
   - Make the chatbot more conversational by enabling it to handle follow-up questions seamlessly.
   - Improve natural language understanding to deliver more interactive and engaging user experiences.

4. **Simplified Deployment**:
   - Create a Docker image to streamline the installation and deployment process, making it easier for users to set up the project.

5. **Multi-Language Support**:
    - Expand the chatbot's language capabilities to support multiple languages, making it suitable for a global audience.

These future enhancements aim to make the RAG chatbot more robust, efficient, and versatile, further enriching the user experience and extending its applicability.

## References and Citations

1. **OpenAI API**: This project uses OpenAI's language models via API. For more information, visit [OpenAI](https://openai.com/).
2. **Chroma DB**: Chroma DB is used as the vector database. Learn more at the [Chroma DB GitHub Repository](https://github.com/chroma-core/chroma).
3. **Hugging Face**: The project leverages pre-trained models and is hosted on Hugging Face Spaces. Visit [Hugging Face](https://huggingface.co/) for more details.
4. **Gradio**: The user interface is built using Gradio. Documentation is available at [Gradio](https://gradio.app/).
5. **LangChain**: Utilities from LangChain are used for document splitting. See [LangChain GitHub](https://github.com/hwchase17/langchain) for more.
6. **PyPDF**: Text extraction from PDFs is performed using PyPDF. For more, check [PyPDF](https://pypdf.readthedocs.io/).

### Data Sources
- Data is sourced from NOV’s publicly available document library and website. All rights and acknowledgments belong to NOV.

### Acknowledgments
- Portions of this documentation were enhanced with the help of language models, including tools like **ChatGPT** by OpenAI.

## Contact

For any questions, feedback, or collaboration inquiries, feel free to reach out:

- **Name**: Dheeraj Chillamcharla
- **Email**: [chillamcharladheeraj@gmail.com](mailto:chillamcharladheeraj@gmail.com)

Feel free to reach out for collaborations or questions—I’d love to hear from you and explore new possibilities together!








