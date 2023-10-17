from PyQt5.QtWidgets import QApplication
from design import MainWindow
from logic import initialize_qa

if __name__ == "__main__":
    app = QApplication([])

    # Initialize the logic
    initialize_qa()

    # Create and show the main window
    window = MainWindow()
    window.show()

    app.exec_()