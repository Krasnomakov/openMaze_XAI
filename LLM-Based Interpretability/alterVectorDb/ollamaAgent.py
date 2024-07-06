from langchain.llms import Ollama
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Initialize Ollama
ollama = Ollama(base_url='http://localhost:11434', model='llama2')

# Load context from web
loader = WebBaseLoader('https://telegra.ph/Shinlap-Program-09-22')
data = loader.load()

# Split the context into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Create a vectorstore from the chunks
vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

# Create a QA chain
qachain = RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())

def get_user_input():
    question = input("Enter your question: ")
    return question

def main():
    while True:
        question = get_user_input()
        if question.lower() == "exit":
            break

        result = qachain({"query": question})
        print(result['result'])  # Display the response

if __name__ == "__main__":
    main()
