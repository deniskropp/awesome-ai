from PyQt5.QtCore import QObject, pyqtSignal


class Chat(QObject):
    newMessage = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.assistants = {}
        self.messages = []

    def add_assistant(self, assistant):
        print(f"Adding assistant: {assistant.name}")
        self.assistants[assistant.name] = assistant

    def remove_assistant(self, name):
        if name in self.assistants:
            del self.assistants[name]

    def send_message(self, sender, content):
        self.messages.append({"role": sender, "content": content})

        self.newMessage.emit()

    def get_messages(self):
        return self.messages
