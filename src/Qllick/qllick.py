from PyQt5 import QtWidgets
from qllama import Qllama
from voice import clone
from playsound import playsound
from AssistantTab import AssistantTab
from ChatTab import ChatTab
from StoryTab import StoryTab
from VoiceTab import VoiceTab


options = { 'temperature': 0.0, 'num_ctx': 1024, 'num_thread': 6 }


class Model():
    def __init__(self, name, size):
        self.name = name
        self.size = size

class ModelsTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
    
        self.parent = parent
        self.qllama = Qllama()

        # List the available models
        self.models = self.qllama.list()

        # Create a table to display the available models
        self.model_list = QtWidgets.QTableWidget()
        self.model_list.setColumnCount(2)
        self.model_list.setHorizontalHeaderLabels(["Name", "Size"])
        self.model_list.setColumnWidth(0, 400)
        self.model_list.setColumnWidth(1, 70)
        self.model_list.setRowCount(len(self.models))

        # Populate the table with model data
        i=0
        for model in self.models:
            print(model)
            self.model_list.setItem(i, 0, QtWidgets.QTableWidgetItem(model['name']))
            # Convert size from bytes to gigabytes and round to 2 decimal places
            size = round(model['size'] / (1024 ** 3), 2)
            self.model_list.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{size} GB"))
            i+=1

        # Create a layout for the tab
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.model_list)
        self.setLayout(layout)

        # Add a list item handler to the model_list table
        self.model_list.itemClicked.connect(self.parent.load_model)



class Application(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        self.qllama = Qllama()

        # List the available models
        self.models = self.qllama.list()

        # Create tabs for each assistant
        self.assistant_tabs = {}

        # Create the models tab
        self.models_tab = ModelsTab(self)
        self.addTab(self.models_tab, "Models")

        # Create the chat pane
        self.chat_tab = ChatTab(self)
        self.addTab(self.chat_tab, "Chat")

        # Create the SD tab
        #self.sd_tab = StableDiffusionTab(self)
        #self.addTab(self.sd_tab, "Stable Diffusion")

        # Create the Voice tab
        self.voice_tab = VoiceTab(self)
        self.addTab(self.voice_tab, "Voice")

        # Create the Story tab
        self.story_tab = StoryTab(self)
        self.addTab(self.story_tab, "Story")

        # Create the promptlayer tab
        #self.promptlayer_tab = PromptLayerTab(self)
        #self.addTab(self.promptlayer_tab, "PromptLayer")

        # Set the window title
        self.setWindowTitle("OLLAMA Multi-Assistant")

        # Resize the window
        self.resize(1400, 960)

    # Load a model from the models tab
    def load_model(self, item):
        # Get the model name from the selected item
        model_name = item.text()
        self.qllama = Qllama(model=model_name)

    # Load an assistant from a file
    def load_assistant(self, name):
        # Create a new tab for the assistant
        tab = AssistantTab(self, name)
        self.assistant_tabs[name] = tab
        self.addTab(tab, name)

    def text_to_speech(self, message_text):
        clone(message_text, "tagesschau.wav", "output.wav")
        playsound("output.wav")



class App:
    def __init__(self):
         self.app = QtWidgets.QApplication([])
         self.window = Application()

    def run(self):
        self.window.show()
        self.app.exec_()

    # Load an assistant from a file
    def load_assistant(self, name):
        self.window.load_assistant(name)



load = [
    'QllickBuzz',
    'Qwick',
#    'Kick La Metta',
#    'Fizz La Metta',
#    'Natalia'
]

if __name__ == "__main__":
    app = App()
    for metta in load:
        app.load_assistant(metta)
    app.run()
