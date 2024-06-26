from flask import Flask, request, jsonify, render_template
import json
from langchain.llms import Ollama
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

app_qa = Flask(__name__)

# Initialize Ollama
ollama = Ollama(base_url='http://localhost:11434', model='llama2')

# File to load context data
data_file_path = "/Users/krasnomakov/Documents1/py/XAI/alterVectorDb/context_data.json"

# Load context from the file using JSONLoader
loader = JSONLoader(
    file_path=data_file_path,
    jq_schema='.[]',
    text_content=False
)

data = loader.load()

# Split the context into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Create a vectorstore from the chunks
vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

# Create a QA chain
qachain = RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())

@app_qa.route("/")
def home():
    return render_template("index.html")

@app_qa.route("/api", methods=["POST"])
def api():
    # Get the question from the user input
    question = request.form["question"]
    
    result = qachain({"query": question})
    print(result)

    answer = result['result']  # Extract the string answer from the dictionary

    return render_template("index.html", question=question, answer=answer)

if __name__ == "__main__":
    app_qa.run(port=5003, debug=True)
