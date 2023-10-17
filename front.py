import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import LlamaCpp

load_dotenv()

# Load environment variables
persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_type = os.environ.get('MODEL_TYPE')
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrivateGPT Interface")

         # Add stylesheet
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            
            ...
            """)

             # Create layout and set spacing
        layout = QVBoxLayout()
        layout.setSpacing(20)

        

        # Set widget margins
        layout.setContentsMargins(50, 50, 50, 50)

        self.query_label = QLabel("Enter a query:")
        self.query_input = QLineEdit()
        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.process_query)

        self.result_label = QLabel("Result:")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.query_label)
        layout.addWidget(self.query_input)
        layout.addWidget(self.ask_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def process_query(self):
        query = self.query_input.text()
        result = qa(query)["result"]
        self.result_output.setText(result)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
