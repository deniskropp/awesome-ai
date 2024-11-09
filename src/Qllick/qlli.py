from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown
from Qllick.Chat import Chat


class MessageView(QWidget):
    def __init__(self, parent, chat: Chat):
        super().__init__(parent)
        self.chat = chat

        self.layout = QVBoxLayout(self)

        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)

        self.chat.newMessage.connect(self.update_view)

    def update_view(self):
        html = f"<html><body>"

        # Iterate over the messages and format them as markdown
        for message in self.chat.get_messages():
            html += f"  <div class=\"message\">"
            html += f"    <div class=\"role\">{message['role']}</div>"
            html += f"    <div class=\"content\">{markdown(message['content'])}</div>"
            html += f"  </div>"
            html += f"  <hr>"

        html += '<style>'
        html += '.role {'
        html += '  color: red;'
        html += '}'
        html += '</style>'
        html += '</body></html>'

        self.webview.setHtml(html)
