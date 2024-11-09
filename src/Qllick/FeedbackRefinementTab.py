from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown
from Qllick.qllama import Registry
from Qllick.Assistant import Assistant

from Qllick.qllama import Registry
from Qllick.Assistant import Assistant

# Create a singleton instance of QllamaRegistry
registry = Registry()



standard_prompt_spymaster = '''Try to find a single word hint that can accurately represent and link the {n} given words: "{target_words}". The key is to select a hint that does not cause confusion with other words from the following list: {word_list}.

Your output should be of the following format:

Answer: (a single word here)

'''

## prompts for self-refinement ##
self_refine_feedback_prompt = '''{question_answer}
---
Analyze the quality of the answer. Provide critque to improve the answer. Your feedback:
'''

self_refine_refinement_prompt = '''{question_answer}
---
Feedback: {feedback}
---
Based on your initial answer and the subsequent feedback, revise the answer. Your revised answer:
'''


class FeedbackRefinement:
    def __init__(self, llm):
        self.llm = llm

    def generate_hint(self, target_words, word_list):
        n = len(target_words)
        prompt = standard_prompt_spymaster.format(n=n, target_words=target_words, word_list=word_list)
        response = self.llm.generate(prompt)
        return response.strip().replace("Answer: ", "")

    def get_feedback(self, hint, target_words, word_list):
        question_answer = f"Hint: {hint}\nTarget Words: {target_words}\nWord List: {word_list}"
        prompt = self_refine_feedback_prompt.format(question_answer=question_answer)
        return self.llm.generate(prompt)

    def refine_hint(self, hint, feedback):
        question_answer = f"Hint: {hint}"
        prompt = self_refine_refinement_prompt.format(question_answer=question_answer, feedback=feedback)
        response = self.llm.generate(prompt)
        return response.strip().replace("Answer: ", "")


class FeedbackRefinementTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.feedback_refinement = FeedbackRefinement(None)

        # Create a label to display the assistant's name
        self.name_label = QtWidgets.QLabel('name')#assistant.name)

        # Create a text edit widget to display the prompt
        self.prompt_text = QtWidgets.QTextEdit()
        self.prompt_text.setReadOnly(False)
        # Open the assistant's prompt file and read it into the model_text
        #self.prompt_text.setText(assistant.prompt)
        # Connect the text edit widget to a function to update the assistant's prompt
        self.prompt_text.textChanged.connect(self.update_prompt)

        # Create a text edit widget for the user to input the target words
        self.target_words_text = QtWidgets.QTextEdit()
        self.target_words_text.setPlaceholderText("Enter target words here...")
        self.target_words_text.setMaximumHeight(50)

        # Create a text edit widget for the user to input the word list
        self.word_list_text = QtWidgets.QTextEdit()
        self.word_list_text.setPlaceholderText("Enter word list here...")
        self.word_list_text.setMaximumHeight(50)
        # Create a button to generate a hint
        self.generate_hint_button = QtWidgets.QPushButton("Generate Hint")
        # Connect the button to a function
        self.generate_hint_button.clicked.connect(self.generate_hint)

        # Create a text edit widget to display the generated hint
        self.generated_hint = QtWidgets.QTextEdit()
        self.generated_hint.setReadOnly(True)

        # Create a button to get feedback
        self.get_feedback_button = QtWidgets.QPushButton("Get Feedback")
        # Connect the button to a function
        self.get_feedback_button.clicked.connect(self.get_feedback)

        # Create a text edit widget to display the feedback
        self.feedback_text = QtWidgets.QTextEdit()
        self.feedback_text.setReadOnly(True)

        # Create a button to refine the hint
        self.refine_hint_button = QtWidgets.QPushButton("Refine Hint")
        # Connect the button to a function
        self.refine_hint_button.clicked.connect(self.refine_hint)
        # Create a layout for the assistant tab
        layout = QtWidgets.QVBoxLayout()
        # Add the widgets to the main layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.prompt_text)
        layout.addWidget(self.target_words_text)
        layout.addWidget(self.word_list_text)
        layout.addWidget(self.generate_hint_button)
        layout.addWidget(self.generated_hint)
        layout.addWidget(self.get_feedback_button)
        layout.addWidget(self.feedback_text)
        layout.addWidget(self.refine_hint_button)

        # Set the layout for the assistant tab
        self.setLayout(layout)

    def update_prompt(self):
        self.assistant.prompt = self.prompt_text.toPlainText()

    def generate_hint(self):
        target_words = self.target_words_text.toPlainText().split()
        word_list = self.word_list_text.toPlainText().split()
        hint = self.feedback_refinement.generate_hint(target_words, word_list)
        self.generated_hint.setText(hint)

    def get_feedback(self):
        hint = self.generated_hint.toPlainText()
        target_words = self.target_words_text.toPlainText().split()
        word_list = self.word_list_text.toPlainText().split()
        feedback = self.feedback_refinement.get_feedback(hint, target_words, word_list)
        self.feedback_text.setText(feedback)

    def refine_hint(self):
        hint = self.generated_hint.toPlainText()
        feedback = self.feedback_text.toPlainText()
        refined_hint = self.feedback_refinement.refine_hint(hint, feedback)
        self.generated_hint.setText(refined_hint)
