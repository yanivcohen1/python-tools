# main.py
import chromadb
import os

class ChromaDBManager:
    """
    A class to manage interactions with a ChromaDB vector database,
    including populating it with text from a file and performing searches.
    """

    def __init__(self, path="chroma_db"):
        """
        Initializes the ChromaDBManager.

        Args:
            path (str): The path to the ChromaDB database directory.
        """
        # Initialize the ChromaDB client with the specified path
        self.client = chromadb.PersistentClient(path=path)
        # Create or get the collection named "text_collection"
        self.collection = self.client.get_or_create_collection(name="text_collection")

    def populate_from_file(self, file_path):
        """
        Populates the ChromaDB database with text from a given file.
        Each line in the file is treated as a separate document.

        Args:
            file_path (str): The path to the text file.
        """
        try:
            with open(file_path, 'r') as f:
                # Read all lines from the file
                lines = f.readlines()
                # Prepare the documents and their corresponding IDs
                documents = [line.strip() for line in lines]
                ids = [f"doc_{i}" for i in range(len(documents))]

                # Add the documents to the collection
                self.collection.add(
                    documents=documents,
                    ids=ids
                )
                print(f"Successfully populated the database with {len(documents)} documents from {file_path}")
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def search(self, query, n_results=5):
        """
        Searches the ChromaDB database for a given query.

        Args:
            query (str): The query string to search for.
            n_results (int): The number of results to return.

        Returns:
            list: A list of the most relevant documents.
        """
        try:
            # Query the collection
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

if __name__ == "__main__":
    # Define the path for the sample text file
    sample_file = "sample_text.txt"

    # Create the sample text file
    create_sample_file(sample_file)

    # Initialize the ChromaDB manager
    db_manager = ChromaDBManager()

    # Populate the database from the sample file
    db_manager.populate_from_file(sample_file)

    # Perform a search
    search_query = "What is Gemini?"
    search_results = db_manager.search(search_query)

    # Print the search results
    print(f"\nSearch results for: '{search_query}'")
    if search_results:
        for i, result in enumerate(search_results):
            print(f"{i+1}. {result}")
    else:
        print("No results found.")

    # Clean up the created files and directory
    os.remove(sample_file)
    # Note: To fully clean up, you would also remove the 'chroma_db' directory.
    # import shutil
    # if os.path.exists("chroma_db"):
    #     shutil.rmtree("chroma_db")
    # print("\nCleaned up sample file and database directory.")
