from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown

from Qllick.qllama import Registry
from Qllick.Assistant import Assistant

# Create a singleton instance of QllamaRegistry
registry = Registry()


class AssistantTab(QtWidgets.QWidget):
    def __init__(self, parent, assistant: Assistant):
        super().__init__(parent)
        self.assistant = assistant
        self.parent = parent

        # Create a label to display the assistant's name
        self.name_label = QtWidgets.QLabel(assistant.name)

        # Create a text edit widget to display the prompt
        self.prompt_text = QtWidgets.QTextEdit()
        self.prompt_text.setReadOnly(False)
        # Open the assistant's prompt file and read it into the model_text
        self.prompt_text.setText(assistant.prompt)
        # Connect the text edit widget to a function to update the assistant's prompt
        self.prompt_text.textChanged.connect(self.update_prompt)

        # Create a text edit widget for the user to input the prompt to generate a response
        self.generate_prompt_text = QtWidgets.QTextEdit()
        self.generate_prompt_text.setPlaceholderText("Enter your prompt here...")
        self.generate_prompt_text.setMaximumHeight(50)

        # Create a button to generate a response
        self.generate_button = QtWidgets.QPushButton("Generate Response")
        # Connect the button to a function
        self.generate_button.clicked.connect(self.generate_response)

        # Create a widget to display the generated output
        self.generated_output = QWebEngineView()
        self.generated_output.setMinimumHeight(300)

        # Create a layout for the assistant tab
        layout = QtWidgets.QVBoxLayout()

        # Create a horizontal layout for the model selection
        model_layout = QtWidgets.QHBoxLayout()
        model_label = QtWidgets.QLabel("Model:")
        self.model_combobox = QtWidgets.QComboBox()
        self.model_combobox.currentTextChanged.connect(self.update_model)

        # Load model list from ollama.list()
        models = registry.list_models()
        self.model_combobox.addItems(models)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combobox)

        # Create a horizontal layout for the temperature control
        temperature_layout = QtWidgets.QHBoxLayout()
        temperature_label = QtWidgets.QLabel("Temperature:")
        self.temperature_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(2000)
        self.temperature_slider.setValue(0)
        temperature_layout.addWidget(temperature_label)
        temperature_layout.addWidget(self.temperature_slider)

        # Create a horizontal layout for the num_ctx control
        num_ctx_layout = QtWidgets.QHBoxLayout()
        num_ctx_label = QtWidgets.QLabel("Num Ctx:")
        self.num_ctx_spinbox = QtWidgets.QSpinBox()
        self.num_ctx_spinbox.setMinimum(0)
        self.num_ctx_spinbox.setMaximum(1024*1024)
        self.num_ctx_spinbox.setValue(1024)
        num_ctx_layout.addWidget(num_ctx_label)
        num_ctx_layout.addWidget(self.num_ctx_spinbox)

        # Create a horizontal layout for the num_predict control
        num_predict_layout = QtWidgets.QHBoxLayout()
        num_predict_label = QtWidgets.QLabel("Num Predict:")
        self.num_predict_spinbox = QtWidgets.QSpinBox()
        self.num_predict_spinbox.setMinimum(0)
        self.num_predict_spinbox.setMaximum(1024*1024)
        self.num_predict_spinbox.setValue(1024)
        num_predict_layout.addWidget(num_predict_label)
        num_predict_layout.addWidget(self.num_predict_spinbox)

        # Add the widgets to the main layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.prompt_text)
        layout.addLayout(model_layout)
        layout.addLayout(temperature_layout)
        layout.addLayout(num_ctx_layout)
        layout.addLayout(num_predict_layout)
        layout.addWidget(self.generate_prompt_text)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.generated_output)

        # Set the layout for the assistant tab
        self.setLayout(layout)

    def update_prompt(self):
        self.assistant.prompt = self.prompt_text.toPlainText()

    def update_model(self):
        self.assistant.model = self.model_combobox.currentText()

    def generate_response(self):
        prompt = self.generate_prompt_text.toPlainText()
        system = self.prompt_text.toPlainText()
        options = {
            'temperature': self.temperature_slider.value()/1000,
            'num_ctx': self.num_ctx_spinbox.value(),
            'num_predict': self.num_predict_spinbox.value(),
            'num_thread': 6,
        }
        response = self.parent.generate(self.model_combobox.currentText(),
                                        prompt, system, options)
        self.generated_output.setHtml(f"<div>\n\n{markdown(response)}\n\n</div>")
