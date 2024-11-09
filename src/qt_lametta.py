from qllama import Qllama
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown


options = {"temperature": 0.1, "num_gpu": 99}



class MarkdownView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)

        self.all_text = "# New chat"
        self.webview.setHtml(markdown(''))

    def set_markdown(self, markdown_text):
        html = markdown(markdown_text)
        self.webview.setHtml(html)

    def append(self, markdown_text):
        self.all_text = f"{self.all_text}\n\n----\n\n{markdown_text}"
        self.set_markdown(self.all_text)


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
        # Open a file and read it into the model_text
        file_path = f"./src/{model_name}/prompt/System Instructions.txt"
        with open(file_path, 'r') as f:
            self.model_text.setText(f.read())


class ChatPane(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.chat_output = MarkdownView()
        self.chat_output.setMinimumHeight(900)
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

class Application(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        self.qllama = Qllama()

        # List the available models
        self.models = self.qllama.list()

        # Create tabs for each assistant
        self.assistant_tabs = {}

        # Create the chat pane
        self.chat_pane = ChatPane(self)
        self.addTab(self.chat_pane, "Chat")

        # Set the window title
        self.setWindowTitle("OLLAMA Multi-Assistant")

        # Resize the window
        self.resize(1600, 1000)

    # Load an assistant from a file
    def load_assistant(self, name):
        # Create a new tab for the assistant
        tab = AssistantTab(self, name)
        self.assistant_tabs[name] = tab
        self.addTab(tab, name)

    def send_message(self, message_text):
        #self.chat_pane.chat_output.clear()
        if (message_text != ''):
            self.chat_pane.chat_output.append(f"#### Denis: {message_text}\n\n")
        all=f"...'''{self.chat_pane.chat_output.all_text}'''"
        for assistant_name, tab in self.assistant_tabs.items():
            response = self.qllama.generate(
                prompt=f"{all}\n\n----\n\n#### {assistant_name}: ",
                system=tab.model_text.toPlainText(),
                options=options,
            )
            self.chat_pane.chat_output.append(f"#### {assistant_name}\n{response['response']}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Application()
    for metta in ['KickBuzz']:#,'Kick La Metta']:
        window.load_assistant(metta)
    window.show()
    app.exec_()
