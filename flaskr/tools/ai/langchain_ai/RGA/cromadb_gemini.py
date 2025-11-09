# main.py
import chromadb
import os
import google.generativeai as genai
import shutil

# --- IMPORTANT ---
# Configure your Gemini API Key here.
# It's recommended to use environment variables for security.
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Replace "YOUR_API_KEY" with your actual key.

db_path = "./chrome_langchain_db"
current_path = os.path.dirname(os.path.abspath(__file__))
docs_path = current_path + "/../content/docs/"


class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    """
    Custom embedding function using the Gemini API to generate embeddings.
    This allows ChromaDB to use Google's state-of-the-art models for vector representation.
    """
    def __call__(self, input_texts: chromadb.Documents) -> chromadb.Embeddings:
        """
        Generates embeddings for a list of documents.

        Args:
            input_texts (chromadb.Documents): A list of text documents to embed.

        Returns:
            chromadb.Embeddings: A list of embeddings corresponding to the input documents.
        """
        model = 'models/embedding-001'  # The model optimized for retrieval embeddings
        # The task_type is crucial for generating the right type of embeddings
        response = genai.embed_content(model=model,
                                       content=input_texts,
                                       task_type="retrieval_document")
        return response["embedding"]


class ChromaDBManager:
    """
    A class to manage interactions with a ChromaDB vector database,
    including populating it with text from a file and performing searches
    using Gemini as the embedding model.
    """

    def __init__(self, path="chroma_db_gemini", collection_name="text_collection_gemini"):
        """
        Initializes the ChromaDBManager.

        Args:
            path (str): The path to the ChromaDB database directory.
        """
        self.client = chromadb.PersistentClient(path=path)

        # Instantiate our custom Gemini embedding function
        gemini_ef = GeminiEmbeddingFunction()

        # Create or get the collection, specifying the custom embedding function
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=gemini_ef
        )

    def populate_from_file(self, file_path):
        """
        Populates the ChromaDB database with text from a given file.
        Each line in the file is treated as a separate document.

        Args:
            file_path (str): The path to the text file.
        """
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                # Filter out any empty lines
                documents = [line.strip() for line in lines if line.strip()]
                if not documents:
                    print("The file is empty or contains only whitespace.")
                    return

                ids = [f"doc_{i}" for i in range(len(documents))]

                # Add the documents to the collection. ChromaDB will automatically
                # use the GeminiEmbeddingFunction to create vectors.
                self.collection.add(
                    documents=documents,
                    ids=ids
                )
                print(f"Successfully populated the database with {len(documents)} documents from {file_path}")
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred during population: {e}")

    def search(self, query, n_results=5):
        """
        Searches the ChromaDB database for a given query.
        The query text will be embedded using the Gemini model before searching.

        Args:
            query (str): The query string to search for.
            n_results (int): The number of results to return.

        Returns:
            list: A list of the most relevant documents.
        """
        try:
            # Query the collection. The query text is automatically embedded.
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results['documents'][0]
        except Exception as e:
            print(f"An error occurred during search: {e}")
            return []

def create_sample_file(file_path="sample_text.txt"):
    """Creates a sample text file for demonstration purposes."""
    content = [
        "The sky is blue and the sun is bright.",
        "Artificial intelligence is transforming many industries.",
        "Python is a versatile programming language.",
        "Vector databases are used for similarity searches.",
        "Gemini is a large language model from Google."
    ]
    with open(file_path, 'w') as f:
        for line in content:
            f.write(line + "\n")
    print(f"Created sample file at {file_path}")

def is_collection_exist(collection_name: str) -> bool:
    vector_store = chromadb.PersistentClient(path=db_path)
    try:
        collection = vector_store.get_collection(collection_name)
        print(f"Collection '{collection_name}' found.")
        return True
    except Exception as e:
        print(f"Collection '{collection_name}' not found.")
        return False

if __name__ == "__main__":
    # Define paths
    sample_file = docs_path + "sample_text_for_gemini.txt"
    # db_path = "chroma_db_gemini"
    collection_name = "text_collection_gemini"
    # Create the sample text file
    collection_exist = is_collection_exist(collection_name)
    # Initialize the ChromaDB manager with Gemini embeddings
    db_manager = ChromaDBManager(path=db_path, collection_name=collection_name)
    if not collection_exist:
        create_sample_file(sample_file)
        # Populate the database from the sample file
        db_manager.populate_from_file(sample_file)
    else:
        print(f"Collection '{collection_name}' already exists. Skipping population.")

    # Perform a search
    search_query = "What is Gemini?"
    search_results = db_manager.search(search_query, 1)

    # Print the search results
    print(f"\nSearch results for: '{search_query}'")
    if search_results:
        for i, result in enumerate(search_results):
            print(f"{i+1}. {result}")
    else:
        print("No results found.")

    # --- Clean up created files and directory ---
    # if os.path.exists(sample_file):
    #     os.remove(sample_file)
    # if os.path.exists(db_path):
    #     shutil.rmtree(db_path)
    # print(f"\nCleaned up sample file and database directory ('{db_path}').")
