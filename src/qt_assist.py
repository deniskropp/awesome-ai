import os
import ast
import ollama
from PyQt5 import QtWidgets, QtGui

std_prompts = [
    '<|start_header_id|>Which parts of the prompt are superfluous or less relevant?<|end_header_id|>',
]

options = {"temperature": 0.0, "num_gpu": 1}

class AssistantTab(QtWidgets.QWidget):
    def __init__(self, parent, model_name):
        super().__init__(parent)
        self.parent = parent
        self.model_name = model_name
        self.model_label = QtWidgets.QLabel(model_name)
        self.model_text = QtWidgets.QTextEdit()
        self.model_text.setReadOnly(False)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_text)
        self.setLayout(layout)

class ChatPane(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.chat_output = QtWidgets.QTextEdit()
        self.chat_output.setReadOnly(True)
        self.message_input = QtWidgets.QTextEdit()
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.chat_output)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

    def send_message(self):
        message_text = self.message_input.toPlainText()
        self.parent.send_message(message_text)

class OpenAIApplication(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        # Read the API key from the environment variable
        # openai.api_key = os.environ.get("AIML_API_KEY")
        # openai.api_base = "https://api.aimlapi.com/v1"

        # List the available models
        self.models = ollama.list()

        # Create tabs for each assistant
        self.assistant_tabs = {}
        for model in self.models['models']:
            tab = AssistantTab(self, model['name'])
            self.assistant_tabs[model['name']] = tab
            self.addTab(tab, model['name'])

        # Create the chat pane
        self.chat_pane = ChatPane(self)
        self.addTab(self.chat_pane, "Chat")

        # Set the window title
        self.setWindowTitle("OLLAMA Multi-Assistant")

        # Resize the window
        self.resize(800, 600)

    def send_message(self, message_text):
        self.chat_pane.chat_output.append(f"User: {message_text}")
        for model_name, tab in self.assistant_tabs.items():
            response = ollama.generate(
                model=model_name,
                prompt=message_text,
                system=tab.model_text.toPlainText(),
                options=options,
            )
            self.chat_pane.chat_output.append(f"{model_name}: {response['response']}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = OpenAIApplication()
    window.show()
    app.exec_()
