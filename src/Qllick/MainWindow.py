import asyncio
from PyQt5 import QtCore, QtWidgets
from voice import clone
from playsound import playsound
from qllama import Registry
from AssistantTab import AssistantTab
from Chat import Chat
#from ChatTab import ChatTab
from FeedbackRefinementTab import FeedbackRefinementTab
from ModelsTab import ModelsTab
from StoryTab import StoryTab
from SyncUpTab import SyncUpTab
from VoiceTab import VoiceTab
from Worker import Worker

# Create a singleton instance of QllamaRegistry
registry = Registry()


class MainWindow(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        # Create worker
        self.worker = Worker()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.worker.finished.connect(self.on_work_finished)

        # Create a chat object
        self.chat = Chat()

        # Create the models tab
        self.models_tab = ModelsTab(self)
        self.addTab(self.models_tab, "Models")

        # Create the chat tab
        #self.chat_tab = ChatTab(self, self.chat)
        #self.addTab(self.chat_tab, "Chat")

        # Create the SD tab
        #self.sd_tab = StableDiffusionTab(self)
        #self.addTab(self.sd_tab, "Stable Diffusion")

        # Create the Voice tab
        self.voice_tab = VoiceTab(self)
        self.addTab(self.voice_tab, "Voice")

        # Create the Story tab
        self.story_tab = StoryTab(self)
        self.addTab(self.story_tab, "Story")

        # Create the SyncUp tab
        self.syncup_tab = SyncUpTab(self)
        self.addTab(self.syncup_tab, "SyncUp")

        # Create the FeedbackRefinement tab
        self.feedbackrefinement_tab = FeedbackRefinementTab(self)
        self.addTab(self.feedbackrefinement_tab, "FeedbackRefinement")

        # Create the promptlayer tab
        #self.promptlayer_tab = PromptLayerTab(self)
        #self.addTab(self.promptlayer_tab, "PromptLayer")

        # Set the window title
        self.setWindowTitle("OLLAMA Multi-Assistant")

        # Resize the window
        self.resize(1660, 960)

    # Add an assistant
    def add_assistant(self, assistant):
        # Add the assistant to the chat object
        self.chat.add_assistant(assistant)

        # Create a new tab for the assistant
        tab = AssistantTab(self, assistant=assistant)
        self.addTab(tab, assistant.name)

    def text_to_speech(self, message_text):
        clone(message_text, "tagesschau.wav", "output.wav")
        playsound("output.wav")

    def generate(self, model, prompt, system, options):
        print("Generating response...")
        # Start worker
        #asyncio.run_coroutine_threadsafe(self.worker.do_work(model, prompt, system, options), self.loop)
        m = registry.get_model(model)
        return m.generate(prompt, system, options)

    def on_work_finished(self, response):
        print(response)
        # Update the UI with the response
        self.update_response(response)
        # Convert the response to speech
        #self.text_to_speech(self.worker.response)
