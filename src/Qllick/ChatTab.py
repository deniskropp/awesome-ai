from PyQt5 import QtWidgets
from markdown import markdown
from Qllick.qllama import Qllama
from Qllick.qlli import MessageView
from Qllick.Assistant import Assistant
from Qllick.Chat import Chat


class ChatTab(QtWidgets.QWidget):
    def __init__(self, parent, chat: Chat):
        super().__init__(parent)
        self.chat = chat

        self.chat_output = MessageView(self, chat)
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
            self.chat.send_message("user", message_text)

        for name in self.chat.assistants:
            qllama = Qllama(base_url='http://127.0.0.1:11434', model=self.chat.assistants.get(name).model)
            response = qllama.chat(
                messages=self.chat.get_messages(),
                system=self.chat.assistants[name].prompt,
            )
            self.chat.send_message('assistant', f"{response}")
