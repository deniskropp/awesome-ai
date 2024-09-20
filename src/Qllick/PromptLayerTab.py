from PyQt5 import QtWidgets
from qllama import Qllama
from qlli import MessageView

from promptlayer import PromptLayer

options = {"temperature": 0.1, "num_gpu": 99, "num_ctx": 256}


class PromptLayerTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.promptlayer_client = PromptLayer()

        self.template_list = QtWidgets.QListWidget()
        self.chat_output = MessageView()
        self.chat_output.setMinimumHeight(900)
        self.message_input = QtWidgets.QTextEdit()
        self.send_button = QtWidgets.QPushButton("Send")
#        self.send_button.clicked.connect(self.send_message)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.template_list)
        layout.addWidget(self.chat_output)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

#        self.load_templates()

    def load_templates(self):
        templates = self.promptlayer_client.templates.all()

        for template in templates:
            self.template_list.addItem(template['prompt_name'])

    def template_selected(self, item):
        template_name = item.text()

        template = self.promptlayer_client.templates.get(template_name)

        # Assuming the parent class has a method to set the current prompt
        self.parent.set_current_prompt(template['prompt'])

        # Connect the template_selected method to the itemClicked signal of the template_list
        self.template_list.itemClicked.connect(self.template_selected)

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
