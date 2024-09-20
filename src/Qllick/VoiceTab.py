from PyQt5 import QtWidgets
from voice import clone
from playsound import playsound


class VoiceTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.play_text = QtWidgets.QTextEdit()
        self.play_button = QtWidgets.QPushButton("Play")
        self.play_button.clicked.connect(self.play_text_content)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.play_text)
        layout.addWidget(self.play_button)
        self.setLayout(layout)

    def play_text_content(self):
        text_to_play = self.play_text.toPlainText()
        clone(text_to_play, "tagesschau.wav", "output.wav")
        playsound("output.wav")
