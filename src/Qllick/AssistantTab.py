from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown

from qllama import Qllama

from colorama import Fore, Back, Style


class AssistantTab(QtWidgets.QWidget):
    def __init__(self, parent, assistant_name):
        super().__init__(parent)
        self.parent = parent
        self.name = assistant_name

        # Create a label to display the assistant's name
        self.name_label = QtWidgets.QLabel(self.name)

        # Create a text edit widget to display the prompt
        self.prompt_text = QtWidgets.QTextEdit()
        self.prompt_text.setReadOnly(False)
        # Open the assistant's prompt file and read it into the model_text
        with open(f"./{self.name}/prompt/System Instructions.txt", 'r') as f:
            self.prompt_text.setText(f.read())

        # Create a button to generate a response
        self.generate_button = QtWidgets.QPushButton("Generate Response")
        # Connect the button to a function
        self.generate_button.clicked.connect(self.generate_response)

        # Create a widget to display the generated output
        self.generated_output = QWebEngineView()
        self.generated_output.setMinimumHeight(400)

        # Create a layout for the assistant tab
        layout = QtWidgets.QVBoxLayout()

        # Create a horizontal layout for the model selection
        model_layout = QtWidgets.QHBoxLayout()
        model_label = QtWidgets.QLabel("Model:")
        self.model_combobox = QtWidgets.QComboBox()

        # Load model list from ollama.list()
        qllama = Qllama(base_url='http://127.0.0.1:11434')
        models = [model['name'] for model in qllama.list()]
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
        self.num_ctx_spinbox.setMaximum(2048)
        self.num_ctx_spinbox.setValue(1024)
        num_ctx_layout.addWidget(num_ctx_label)
        num_ctx_layout.addWidget(self.num_ctx_spinbox)

        # Create a horizontal layout for the num_predict control
        num_predict_layout = QtWidgets.QHBoxLayout()
        num_predict_label = QtWidgets.QLabel("Num Predict:")
        self.num_predict_spinbox = QtWidgets.QSpinBox()
        self.num_predict_spinbox.setMinimum(0)
        self.num_predict_spinbox.setMaximum(2048)
        self.num_predict_spinbox.setValue(500)
        num_predict_layout.addWidget(num_predict_label)
        num_predict_layout.addWidget(self.num_predict_spinbox)

        # Add the widgets to the main layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.prompt_text)
        layout.addLayout(model_layout)
        layout.addLayout(temperature_layout)
        layout.addLayout(num_ctx_layout)
        layout.addLayout(num_predict_layout)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.generated_output)

        # Set the layout for the assistant tab
        self.setLayout(layout)

    def generate_response(self):
        qllama = Qllama(base_url='http://127.0.0.1:11434', model=self.model_combobox.currentText())
        #qlloma = Qlloma()
        prompt = self.prompt_text.toPlainText()
        options = {
            'temperature': self.temperature_slider.value()/1000,
            'num_ctx': self.num_ctx_spinbox.value(),
            'num_predict': self.num_predict_spinbox.value(),
        }
        response = qllama.generate_raw(prompt, options)
        #response = qlloma.generate_response(prompt, options)
        self.generated_output.setHtml(f"<div>\n\n{markdown(response)}\n\n</div>")
