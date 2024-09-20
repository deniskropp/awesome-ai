from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown

class MessageView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)

        self.messages = []

    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})
        self.update_view()

    def set_markdown(self, markdown_text):
        html = f"<html><body>{markdown(markdown_text)}</body></html>"
        self.webview.setHtml(html)

    def update_view(self):
        html = f"<html><body>"

        # Iterate over the messages and format them as markdown
        for message in self.messages:
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
