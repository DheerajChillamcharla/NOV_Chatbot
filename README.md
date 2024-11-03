# RAG Chat Bot for NOV

## Introduction 

This project is a Retrieval-Augmented Generation (RAG) question-and-answer chatbot specifically designed to deliver precise and relevant information about NOV’s products. The chatbot uses OpenAI models via API integration to effectively answer queries related to product details, brochures, flyers, catalogs, case studies, and more. By leveraging both retrieval and generation techniques, the bot ensures comprehensive and accurate responses, drawing from NOV’s extensive and openly available document library. This targeted approach provides a streamlined user experience, enabling efficient access to product-related information.

## Features

- **Product-Focused Q&A**: Specially designed to answer questions about NOV’s products, including technical specifications, use cases, and detailed descriptions sourced from the document library.
- **OpenAI API Integration**: Leverages powerful OpenAI models to generate accurate and contextually relevant responses, ensuring high-quality answers for users' queries.
- **Document Retrieval**: Uses advanced retrieval techniques to extract information from NOV’s publicly available resources, such as brochures, flyers, catalogs, and case studies.
- **Efficient Information Access**: Quickly fetches and presents relevant content, reducing the time and effort required to navigate the extensive NOV document library manually.
- **Dynamic Knowledge Base**: Supports continuous updates and improvements, enabling the chatbot to remain aligned with the latest product information and company resources.
- **Robust Error Handling**: Designed to handle ambiguous or unclear queries gracefully, offering suggestions or prompts for clarification to improve the user experience.
- **Customizable and Scalable**: Built to accommodate future enhancements and expansions, allowing the integration of additional features or new data sources as needed.

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
- [Contributing](#contributing)
- [License](#license)
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

### Benefits of This Retrieval Approach

- **High Accuracy**: By using MMR and optimized search parameters, the retrieval system ensures that responses are accurate and relevant.
- **Broad Information Scope**: The diversity element in MMR enables the chatbot to consider a wide range of information, resulting in more well-rounded answers.
- **Efficiency and Scalability**: The locally hosted vector database and efficient retrieval algorithms make the system highly scalable, capable of handling extensive datasets.

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

### Benefits of the Augmenting Process
- **Increased Accuracy**: By providing additional context and strict instructions, the model generates precise answers without straying from verified information.
- **Enhanced Credibility**: Including reference links makes the response more trustworthy and allows users to verify or further explore the information.
- **Focused Information**: The model is explicitly instructed to only discuss NOV and its products, ensuring that all answers are relevant and aligned with the project's goals.
- **Efficiency**: Through prompt engineering, the augmenting process optimizes the use of the language model, reducing the need for repeated queries and improving the overall user experience.

This well-designed augmenting process is key to delivering high-quality, contextually rich responses from the RAG chatbot.








