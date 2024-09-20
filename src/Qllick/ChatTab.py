from PyQt5 import QtWidgets
from markdown import markdown
from qllama import Qllama
from qlli import MessageView

class ChatTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.chat_output = MessageView()
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

        if (message_text != ''):
            self.chat_output.add_message("Denis", message_text)

        for assistant_name, tab in self.parent.assistant_tabs.items():
            qllama = Qllama(base_url='http://127.0.0.1:11434', model=tab.model_combobox.currentText())
            response = qllama.chat(
                messages=self.chat_output.messages,
                system=tab.prompt_text.toPlainText(),
            )
            self.chat_output.add_message(assistant_name, f"{response}")
