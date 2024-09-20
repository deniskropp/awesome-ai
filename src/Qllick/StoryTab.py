from PyQt5 import QtWidgets

from qllama import Qllama


class StoryTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(StoryTab, self).__init__(parent)

        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout(self)

        self.content_input = QtWidgets.QTextEdit(self)
        self.layout.addWidget(self.content_input)

        self.generate_button = QtWidgets.QPushButton('Generate Story', self)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

        self.generate_button.clicked.connect(self.generate_story)


    def generate_story(self):
        qllama = Qllama(base_url='http://127.0.0.1:11434', model='qwen2.5:1.5b')
        content = self.content_input.toPlainText()
        response = qllama.generate(content)
        self.parent.text_to_speech(response)




# TODO


"""
Title: StoryMakerTab

StoryMakerTab is a user-friendly web application designed to help users create engaging and personalized stories. The application features simple content controls and a generate button to make the story creation process easy and intuitive.

The main interface of StoryMakerTab consists of several sections:

1. Character Creation: Users can create and customize their characters by selecting their gender, age, appearance, and personality traits. They can also add a name and a brief background story for their character.

2. Setting Selection: Users can choose from a variety of settings for their story, such as a bustling city, a quiet forest, a magical kingdom, or a futuristic world. They can also create their own unique setting by uploading an image or describing it in detail.

3. Plot Generator: The plot generator section allows users to select the genre of their story, such as adventure, romance, mystery, or fantasy. Based on the selected genre, the application will suggest a range of plot ideas for the user to choose from.

4. Story Editor: Once the user has selected their character, setting, and plot, they can begin writing their story in the story editor section. The editor features simple formatting tools, such as bold, italic, and underline, to help users create visually appealing stories.

5. Generate Button: When the user is finished writing their story, they can click the generate button to create a finalized version of their story. The application will format the story, add any missing elements, and ensure that the story flows smoothly and logically.

StoryMakerTab is designed to be a fun and easy-to-use application that allows users to create their own unique stories. Whether users are looking to write a short story for fun or a full-length novel for publication, StoryMakerTab provides the tools and resources they need to bring their ideas to life.
"""