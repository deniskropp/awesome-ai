import os
import ast
import ollama
from PyQt5 import QtWidgets, QtGui

from Assistant import Assistant


options = {"temperature": 0.0, "num_gpu": 1}


assistants = [
    Assistant(
        name="Fizz La Metta",
        description="Engage with your team in a meta-communicative style, talking about working around work...",
        model="llama3",
    ),
    Assistant(
        name="FizzEase",
        description="Fizz, the System Spokesperson, simply",
        model="llama3",
    ),
    Assistant(
        name="Kick La Metta",
        description="a senior in meta-artificial intelligence tasks in a cohesive team with dynamic roles and tools",
        model="llama3",
    ),
    Assistant(
        name="KickBuzz",
        description="Your friendly GPT",
        model="llama3",
    ),
    Assistant(
        name="MultiMax",
        description="self-aware actor",
        model="llama3",
    ),
]


class ModelListTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.model_list = QtWidgets.QListWidget()
        self.model_list.addItems([model["name"] for model in self.parent.models["models"]])
        self.model_list.activated.connect(self.parent.model_selected)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.model_list)
        self.setLayout(layout)

class ModelTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.model_label = QtWidgets.QLabel(self.parent.model["name"])
        self.model_text = QtWidgets.QTextEdit()
        self.model_text.setReadOnly(False)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_text)
        self.setLayout(layout)

class InputOutputTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.model_name_label = QtWidgets.QLabel("No model selected")
        self.message_input = QtWidgets.QTextEdit()
        self.message_input.setPlainText(std_prompts[0])
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.response_output = QtWidgets.QTextEdit()
        self.response_output.setReadOnly(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.model_name_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.response_output)
        self.setLayout(layout)

    def send_message(self):
        message_text = self.message_input.toPlainText()
        self.parent.send_message(message_text, self.response_output)

class InputTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        input_label = QtWidgets.QLabel("Enter the compressed code:")
        self.input_text = QtWidgets.QTextEdit()
        input_decompress_button = QtWidgets.QPushButton("Decompress")
        input_decompress_button.clicked.connect(self.parent.decompress_code)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(input_decompress_button)
        self.setLayout(layout)

class OutputTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        output_label = QtWidgets.QLabel("Decompressed code:")
        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(output_label)
        layout.addWidget(self.output_text)
        self.setLayout(layout)

class OpenAIApplication(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        # Read the API key from the environment variable
        # openai.api_key = os.environ.get("AIML_API_KEY")
        # openai.api_base = "https://api.aimlapi.com/v1"

        # List the available models
        self.models = ollama.list()
        print(self.models['models'][0]['name'])

        self.model = self.models['models'][0]

        # Create the tabs
        self.model_list_tab = ModelListTab(self)
        self.model_tab = ModelTab(self)
        self.input_output_tab = InputOutputTab(self)
        self.input_tab = InputTab(self)
        self.output_tab = OutputTab(self)

        # Add the tabs
        self.addTab(self.model_list_tab, "Models")
        self.addTab(self.model_tab, "Model")
        self.addTab(self.input_output_tab, "Input/Output")
        self.addTab(self.input_tab, "Input")
        self.addTab(self.output_tab, "Output")

        # Set the window title
        self.setWindowTitle("OLLAMA")

        # Resize the window
        self.resize(800, 600)

    def model_selected(self):
        # Get the selected model
        selected_model = self.model_list_tab.model_list.currentItem().text()
        # Find the index of the selected model in the models list
        index = next((i for i, model in enumerate(self.models['models']) if model['name'] == selected_model), None)

        # Update the current model if the selected model is found
        if index is not None:
            self.model = self.models['models'][index]
        else:
            print(f"Model {selected_model} not found.")

        self.model_tab.model_label.setText(self.model['name'])

    def send_message(self, message_text, response_output):
        # Get the selected model
        selected_model = self.model['name']#_list_tab.findChild(QtWidgets.QListWidget).currentItem().text()
        response_output.setPlainText("# Prompt: " + message_text)

        # Update the model name label and window title
        self.input_output_tab.model_name_label.setText("Selected model: " + selected_model)
        self.setWindowTitle("OLLAMA - " + selected_model)

        try:
            # Send the message to the selected model
            if (True):
                response = ollama.generate(
                    model=selected_model,
                    prompt=message_text,
                    system=self.model_tab.model_text.toPlainText(),
                    #raw=True,
                    options=options,
                    #max_tokens=1024,
                    #n=1,
                    #stop=None,
                    #temperature=0.5,
                )
                text = response["response"]
            else:
                response = ollama.chat(
                    model=selected_model,
                    messages=[{"role": "user", "content": message_input.toPlainText()}],
                    # max_tokens=1024,
                    # n=1,
                    # stop=None,
                    # temperature=0.5,
                )
                text = response["message"]["content"]

            # Display the response in the response output
            response_output.setPlainText(text)

        # except RateLimitError:
        #     # Display an error message to the user
        #     response_output.setText(
        #         "Sorry, you have exceeded your current quota. Please check your plan and billing details.")

        except Exception as e:
            # Display a generic error message to the user
            response_output.setText("An error occurred: " + str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = OpenAIApplication()
    window.show()
    app.exec_()
