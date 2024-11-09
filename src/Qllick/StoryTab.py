from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown
from .qllama import Registry



"""
Title: StoryMaker

StoryMaker is a user-friendly application designed to help users create engaging and personalized stories. The application features simple content controls and a generate button to make the story creation process easy and intuitive.

The main interface of StoryMaker consists of several sections:

1. Character Creation: Users can create and customize any number of characters by selecting their gender, age, appearance, and personality traits. They can also add a name and a brief background story for their character.

2. Setting Selection: Users can choose from a variety of settings for their story, such as a bustling city, a quiet forest, a magical kingdom, or a futuristic world. They can also create their own unique setting by uploading an image or describing it in detail.

3. Plot Generator: The plot generator section allows users to select the genre of their story, such as adventure, romance, mystery, or fantasy. Based on the selected genre, the application will suggest a range of plot ideas for the user to choose from.

4. Story Editor: Once the user has selected their character, setting, and plot, they can begin writing their story in the story editor section. The editor features simple formatting tools, such as bold, italic, and underline, to help users create visually appealing stories.

5. Generate Button: When the user is finished writing their story, they can click the generate button to create a finalized version of their story. The application will format the story, add any missing elements, and ensure that the story flows smoothly and logically.

StoryMaker is designed to be a fun and easy-to-use application that allows users to create their own unique stories. Whether users are looking to write a short story for fun or a full-length novel for publication, StoryMaker provides the tools and resources they need to bring their ideas to life.
"""

registry = Registry()


class Character:
    def __init__(self, name: str, gender: str, age: int, appearance: str, personality: str, background: str):
        self.name = name
        self.gender = gender
        self.age = age
        self.appearance = appearance
        self.personality = personality
        self.background = background



class StoryTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(StoryTab, self).__init__(parent)

        self.input_layout = QtWidgets.QVBoxLayout()
        self.output_layout = QtWidgets.QVBoxLayout()

        # Create a scroll area
        #scroll_area = QtWidgets.QScrollArea()
        #scroll_area.setWidgetResizable(True)

        # Create a widget to hold the layout
        #scroll_widget = QtWidgets.QWidget()
        #scroll_widget.setLayout(self.input_layout)

        # Set the scroll area's widget to the scroll widget
        #scroll_area.setWidget(scroll_widget)

        # Set the main layout of the StoryTab to the scroll area
        #main_layout = QtWidgets.QVBoxLayout(self)
        #main_layout.addWidget(scroll_area)

        #self.setLayout(main_layout)


        # Characters
        self.character_group = QtWidgets.QGroupBox("Characters")
        self.character_layout = QtWidgets.QVBoxLayout()

        self.characters = []
        self.add_character_button = QtWidgets.QPushButton("Add Character")
        self.add_character_button.clicked.connect(self.add_character)
        self.character_layout.addWidget(self.add_character_button)

        self.character_group.setLayout(self.character_layout)
        self.input_layout.addWidget(self.character_group)

        # Setting
        self.setting_group = QtWidgets.QGroupBox("Setting")
        setting_layout = QtWidgets.QVBoxLayout()

        self.setting_input = QtWidgets.QTextEdit()
        self.setting_input.setPlaceholderText("Describe your setting")
        setting_layout.addWidget(self.setting_input)

        self.setting_group.setLayout(setting_layout)
        self.input_layout.addWidget(self.setting_group)

        # Genre
        self.genre_group = QtWidgets.QGroupBox("Genre")
        genre_layout = QtWidgets.QVBoxLayout()

        self.genre_input = QtWidgets.QTextEdit()
        self.genre_input.setPlaceholderText("Choose a genre")
        genre_layout.addWidget(self.genre_input)

        self.genre_group.setLayout(genre_layout)
        self.input_layout.addWidget(self.genre_group)

        # Plot
        self.plot_group = QtWidgets.QGroupBox("Plot")
        plot_layout = QtWidgets.QVBoxLayout()

        self.plot_input = QtWidgets.QTextEdit()
        self.plot_input.setPlaceholderText("Describe story line")
        plot_layout.addWidget(self.plot_input)

        self.plot_group.setLayout(plot_layout)
        self.input_layout.addWidget(self.plot_group)

        # Add spacing/separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Generate Button
        self.generate_button = QtWidgets.QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_story)
        self.output_layout.addWidget(self.generate_button)

        # Generated Story
        self.story_view = QWebEngineView()
        #self.story_view.setMinimumHeight(800)
        self.story_view.setMinimumWidth(800)
        self.output_layout.addWidget(self.story_view)


        # Create a layout for the tab
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self.input_layout)
        layout.addWidget(separator)
        layout.addLayout(self.output_layout)

        self.setLayout(layout)



    def add_character(self):
        # Create a new character widget and add it to the layout
        new_character = Character("", "", 0, "", "", "")
        new_character_widget = CharacterWidget(self, new_character)
        self.character_layout.insertWidget(self.character_layout.count() - 1, new_character_widget)
        self.characters.append(new_character)

    def generate_story(self):
        # Collect user inputs
        setting = self.setting_input.toPlainText()
        genre = self.genre_input.toPlainText()
        plot = self.plot_input.toPlainText()

        # Generate the final story
        final_story = "Generate 1000 words story based on the following:\n\n"

        for character in self.characters:
            final_story += f"## Character\n"
            final_story += f"- Name: {character.name}\n"
            final_story += f"- Gender: {character.gender}\n"
            final_story += f"- Age: {character.age}\n"
            final_story += f"- Appearance: {character.appearance}\n"
            final_story += f"- Personality: {character.personality}\n"
            final_story += f"- Background: {character.background}\n\n"

        final_story += f"## Setting\n{setting}\n\n"

        final_story += f"## Genre\n{genre}\n\n"

        final_story += f"## Plot\n{plot}\n\n"

        # Generate the story using the model
        model = registry.get_model('gemini-pro')
        generated = model.generate(final_story, 'You are a story writer.', {
            'max_output_tokens': 4000,
            'temperature': 0.8,
            'top_p': 0.95,
        })

        # Display the final story
        self.story_view.setHtml(markdown(generated))


class CharacterWidget(QtWidgets.QWidget):
    def __init__(self, parent, character: Character):
        super(CharacterWidget, self).__init__(parent)
        self.character = character

        layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit(character.name)
        self.name_input.setText(character.name)
        layout.addRow("Name", self.name_input)

        self.gender_input = QtWidgets.QComboBox()
        self.gender_input.addItems(["Male", "Female", "Non-binary"])
        self.gender_input.setCurrentText(character.gender)
        layout.addRow("Gender", self.gender_input)

        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setValue(character.age)
        layout.addRow("Age", self.age_input)

        self.appearance_input = QtWidgets.QTextEdit(character.appearance)
        self.appearance_input.setText(character.appearance)
        layout.addRow("Appearance", self.appearance_input)

        self.personality_input = QtWidgets.QTextEdit(character.personality)
        self.personality_input.setText(character.personality)
        layout.addRow("Personality", self.personality_input)

        self.background_input = QtWidgets.QTextEdit(character.background)
        self.background_input.setText(character.background)
        layout.addRow("Background", self.background_input)

        self.setLayout(layout)


        # Connect the textChanged signal to update the character's attributes
        self.name_input.textChanged.connect(self.update_character_name)
        self.gender_input.currentTextChanged.connect(self.update_character_gender)
        self.age_input.valueChanged.connect(self.update_character_age)
        self.appearance_input.textChanged.connect(self.update_character_appearance)
        self.personality_input.textChanged.connect(self.update_character_personality)
        self.background_input.textChanged.connect(self.update_character_background)

    def update_character_name(self, name):
        self.character.name = name

    def update_character_gender(self, gender):
        self.character.gender = gender

    def update_character_age(self, age):
        self.character.age = age

    def update_character_appearance(self):
        self.character.appearance = self.appearance_input.toPlainText()

    def update_character_personality(self):
        self.character.personality = self.personality_input.toPlainText()

    def update_character_background(self):
        self.character.background = self.background_input.toPlainText()
