import os

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from pypdf import PdfReader


# Keep local Chroma traffic off the machine's HTTP proxy.
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

_collection = None


def _get_collection():
    global _collection

    if _collection is None:
        client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=int(os.getenv("CHROMA_PORT", "8001")),
        )
        _collection = client.get_or_create_collection(
            name="roger_store_docs",
            embedding_function=DefaultEmbeddingFunction(),
        )

    return _collection


def chunk_text(text, chunk_size=500): 
    # current_chunk = [I willl earn python] --> I will learn python
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1

        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
        

def load_documents():
    docs_path = "support/documents/"

    documents = []
    ids = []

    for filename in os.listdir(docs_path):
        if filename.endswith(".pdf"):
            # filepath: support/documents/refund_policy.pdf
            filepath = os.path.join(docs_path, filename)
            reader = PdfReader(filepath)
            
            raw_text = ""
            for page in reader.pages:
                raw_text += page.extract_text()

            chunks = chunk_text(raw_text, chunk_size=500)

            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                ids.append(f"{filename}_{i}")

    if documents:
        _get_collection().add(documents=documents, ids=ids)

    print(f"Loaded {len(documents)} chunks into ChromaDB")
    
        

def search_knowledge_base(query):
    results = _get_collection().query(query_texts=[query], n_results=3)
    print("DEBUG RESULTS:", results["documents"])
    if not results["documents"][0]:
        return "No relevant information found in company documents."
    
    matched_chunks = results["documents"][0]
    return "\n\n".join(matched_chunks)


"""
matched_chunks = [
    "Refund requests must be submitted within 30 days of delivery.",
    "Approved refunds are processed within 7 to 10 business days.",
    "Products purchased during sales are eligible for exchange only."
]


Refund requests must be submitted within 30 days of delivery.

Approved refunds are processed within 7 to 10 business days.

Products purchased during sales are eligible for exchange only.

"""