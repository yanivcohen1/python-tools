import os
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains.retrieval import create_retrieval_chain
# from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter

folder_path = "./chrome_langchain_db"

current_path = os.path.dirname(os.path.abspath(__file__))

docs_path = current_path + "/../content/docs/"

cached_llm = OllamaLLM(model="mxbai-embed-large:335m")

embedding = FastEmbedEmbeddings()

collection_name = "alice_pdf"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=384, chunk_overlap=80, length_function=len, is_separator_regex=False
)

def get_collection_names():
    vector_store = Chroma(persist_directory=folder_path) # , embedding_function=embedding
    collections = vector_store._client.list_collections()
    print(f"collections: {collections}")
    return collections

def del_collection(collection_name: str):
    vector_store = Chroma(persist_directory=folder_path) # , embedding_function=embedding
    vector_store._client.delete_collection(collection_name)
    print(f"deleted collection: {collection_name}")
    return True

def get_chanks_len(collection_name: str):
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding, collection_name=collection_name)
    collection = vector_store._client.get_collection(collection_name)
    result = collection.get()
    doc_size = len(result["documents"][0])
    num_docs = len(result["ids"])
    print(f"chank(doc) size: {doc_size}")
    print(f"docs(chanks) size: {num_docs}")

if __name__ == "__main__":
    get_collection_names()
    # get_chanks_len("alice_pdf") # 573 * 386
    # get_chanks_len("pdf") # 205 * 1024
    # get_chanks_len("restaurant_reviews") # 123 * 386
    # del_collection("alice_pdf")
    # pdf_to_vector("alice.pdf")
    # get_collection_names()
