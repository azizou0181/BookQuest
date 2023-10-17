import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import LlamaCpp

load_dotenv()


def initialize_qa():
     # Load environment variables
    persist_directory = os.environ.get('PERSIST_DIRECTORY')
    model_path = os.environ.get('MODEL_PATH')
    embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')
    model_n_ctx = os.environ.get('MODEL_N_CTX')
    model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))
    target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))

    # Create the LLM
    llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, n_batch=model_n_batch, verbose=False)

    # Create the embeddings
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    # Create the vectorstore retriever
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})

    # Create the retrieval QA chain
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    return qa

def process_query(qa, query):
    if query is None or query.strip() == "":
        return None  # Return None or an appropriate value when the query is empty
    
    result = qa(query)["result"]
    return result

def main():
    qa = initialize_qa()
    # Process queries or perform other actions
    # ...


if __name__ == "__main__":
    main()
