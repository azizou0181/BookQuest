from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton


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
        # Call the logic-related function from the logic.py file
        from logic import process_query
        query = self.query_input.text()
        result = process_query(query)
        self.result_output.setText(result)