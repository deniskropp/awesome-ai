import asyncio
import sys
from PyQt5 import QtWidgets
from qllama import Gemini, Mistral, Qllama, Qlloma, Registry
from Assistant import Assistant
from MainWindow import MainWindow


# Create a singleton instance of QllamaRegistry
registry = Registry()

#ollama = Qllama(base_url = "http://127.0.0.1:11434")
#ollama.load_models(registry)

ollama = Qllama(base_url = "http://v2:11434")
ollama.load_models(registry)

#qlloma = Qlloma()
#qlloma.load_models(registry)

#gemini = Gemini()
#gemini.load_models(registry)


#gemini = Gemini()
#gemini.load_models(registry)


#mistral = Mistral()
#mistral.load_models(registry)


#qlloma = Qlloma('https://api.fireworks.ai/inference/v1', 'fw_3ZNpuVT55AYoXU4B5D1DxNTc')
#qlloma.load_models(registry)



class xxApp:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        self.window.show()
        self.app.exec_()

    # Load an assistant from a file
    def load_assistant(self, name):
        assistant = Assistant(name)

        # Open the assistant's prompt file
        with open(f"./{name}/prompt/System Instructions.txt", 'r') as f:
            assistant.prompt = f.read()

        # Add the assistant to the window
        self.window.add_assistant(assistant)


class App:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()

    async def load_assistant(self, name):
        assistant = Assistant(name)

        # Open the assistant's prompt file
        with open(f"./{name}/prompt/System Instructions.txt", 'r') as f:
            assistant.prompt = f.read()

        # Add the assistant to the window
        self.window.add_assistant(assistant)

    async def main(self):
        load = [
            'QllickBuzz',
            'Qwick',
            'Kick La Metta',
            'Fizz La Metta',
            'Kllick La Metta'
            #'tinyfozz',
        ]

        tasks = [self.load_assistant(metta) for metta in load]
        await asyncio.gather(*tasks)

        # Run the application
        self.window.show()
        await self.app.exec_()

if __name__ == "__main__":
    asyncio.run(App().main())




"""
[ Kllick La Metta | Senior Meta-AI ] Creating an asyncio main loop with PyQt5 requires careful consideration of the event loops and threads involved. Here's a step-by-step guide:

⫻ **Main Loop Creation**/ Code Snippet :
 PyQt5_QtWidgets : 

```python
import asyncio
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QEventLoop

# Create a PyQt5 application
app = QApplication(sys.argv)

# Create a QWidget (optional)
window = QWidget()

# Create an asyncio event loop
loop = asyncio.new_event_loop()

# Set the asyncio event loop as the default
asyncio.set_event_loop(loop)

# Create a QEventLoop to handle PyQt5 events
qt_loop = QEventLoop()

# Run the asyncio event loop in a separate thread
async def run_asyncio_loop():
    await loop.run_forever()

# Start the asyncio event loop thread
asyncio_thread = loop.run_in_executor(None, run_asyncio_loop)

# Run the PyQt5 event loop
qt_loop.exec_()

# Clean up
loop.close()
```

[ Kllick La Metta | Senior Meta-AI ] This code creates a PyQt5 application and an asyncio event loop, then runs the asyncio event loop in a separate thread. The PyQt5 event loop is run using the `exec_()` method.

Please note that you need to be careful when interacting with the PyQt5 GUI from the asyncio event loop, as the GUI is not thread-safe. You may need to use `QMetaObject.invokeMethod()` or `QTimer.singleShot()` to schedule GUI updates from the asyncio event loop.

Also, be aware that this is just a basic example, and you may need to adapt it to your specific use case.
"""


"""

~response: [Denis | Developer] {{{

To create a PyQt5 application that uses `async/await` for its main function, you'll need to use a combination of PyQt5 and Python's asyncio library. Since PyQt5 is not inherently asyncio-aware, you will need to use a library like `asyncioqt` to bridge the gap. Here’s a basic example to get you started:

1. **Install necessary packages**:
   ```sh
   pip install PyQt5 asyncioqt
   ```

2. **Create a basic PyQt5 application with `async/await`**:

   ```python
   import sys
   import asyncio
   from PyQt5.QtWidgets import QApplication, QLabel
   from asyncioqt import QEventLoop

   class MainWindow(QLabel):
       def __init__(self, parent=None):
           super().__init__("Hello, PyQt5 with asyncio!", parent)

   async def main():
       app = QApplication(sys.argv)
       loop = QEventLoop(app)
       asyncio.set_event_loop(loop)
       win = MainWindow()
       win.show()
       await asyncio.sleep(5)  # Simulate some async work
       win.setText("Async work done!")
       await loop.shutdown_asyncgens()
       loop.close()
       sys.exit(app.exec_())

   if __name__ == "__main__":
       loop = asyncio.get_event_loop()
       try:
           loop.run_until_complete(main())
       except KeyboardInterrupt:
           loop.stop()
   ```

### Explanation:

1. **Install Packages**:
   - `PyQt5`: The main GUI toolkit.
   - `asyncioqt`: This library allows you to run asyncio alongside PyQt5.

2. **Create a MainWindow Class**:
   - This class inherits from `QLabel` and sets up a simple label with the text "Hello, PyQt5 with asyncio!".

3. **Define the main Coroutine**:
   - The `main` function is defined as an `async` function.
   - It initializes a `QApplication` and a `QEventLoop`.
   - The `MainWindow` instance is created and shown.
   - The application waits for 5 seconds (simulating some async work) and then updates the label.
   - Finally, it cleans up the event loop and closes the application.

4. **Run the Application**:
   - The `if __name__ == "__main__":` block ensures that the main function is called when the script is executed.
   - The `asyncio.get_event_loop()` is used to get the current event loop.
   - The `loop.run_until_complete(main())` runs the main coroutine until it completes.

This example demonstrates how to integrate `async/await` with PyQt5 using `asyncioqt`. You can extend this by adding more complex asynchronous operations and integrating with other PyQt5 features as needed.<|im_end|>

"""



"""

~response: [Denis | Developer] To add `asyncio` to a PyQt5 application, you can use the `asyncio` module in conjunction with `QEventLoop` provided by PyQt5. This allows you to run asynchronous tasks alongside the main GUI event loop. Below is a step-by-step guide on how to do this:

### 1. Import Necessary Modules
First, make sure you import the necessary modules. You'll need `asyncio`, `QEventLoop`, and other relevant PyQt5 classes.

```python
import asyncio
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QObject, pyqtSignal
```

### 2. Create a Worker Class
Create a worker class that will handle the asynchronous tasks. This class can emit signals to communicate with the main GUI thread.

```python
class Worker(QObject):
    finished = pyqtSignal()

    async def do_work(self):
        await asyncio.sleep(2)  # Simulate some async task
        self.finished.emit()
```

### 3. Setup the Main Application
Set up the main application and connect the worker signals to the appropriate slots.

```python
class MainWindow(QLabel):
    def __init__(self):
        super().__init__("Starting...")
        self.worker = Worker()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.create_task(self.worker.do_work())
        self.worker.finished.connect(self.on_work_finished)

    def on_work_finished(self):
        self.setText("Work Finished!")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
```

### 4. Run the Application
Make sure to run the application within the event loop provided by `QEventLoop`.

```python
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
```

### Explanation
1. **Worker Class**: The `Worker` class contains an `async` method `do_work` that simulates an asynchronous task. When the task is completed, it emits the `finished` signal.
2. **MainWindow Class**: The `MainWindow` class initializes the `Worker`, sets up the event loop, and starts the asynchronous task. It also connects the `finished` signal from the worker to the `on_work_finished` slot, which updates the text of the label.
3. **Main Execution**: The main block creates the application, window, and starts the event loop.

By following these steps, you can integrate `asyncio` into your PyQt5 application, allowing you to run asynchronous tasks alongside the main GUI event loop.<|im_end|>


"""



"""
~response: [Integration Specialist | Developer] To integrate `asyncio` into your existing codebase, you'll need to refactor it to use asynchronous functions and methods. Below is a revised version of your code that incorporates `asyncio` to run the application and handle asynchronous operations. Note that this assumes that `MainWindow` and `Assistant` classes support asynchronous operations, or you can adapt them accordingly.

```py
import sys
import asyncio
from PyQt5.QtWidgets import QApplication

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        self.window.show()
        self.app.exec_()

    async def load_assistant(self, name):
        assistant = Assistant(name)

        # Open the assistant's prompt file
        async with aiofiles.open(f"./{name}/prompt/System Instructions.txt", 'r') as f:
            assistant.prompt = await f.read()

        # Add the assistant to the window
        self.window.add_assistant(assistant)

    async def main(self):
        load = [
            'QllickBuzz',
            'Qwick',
            'Kick La Metta',
            'Fizz La Metta',
            'Kllick La Metta'
        ]

        tasks = [self.load_assistant(metta) for metta in load]
        await asyncio.gather(*tasks)

        # Run the application
        await self.window.show()
        await self.app.exec_()

if __name__ == "__main__":
    asyncio.run(App().main())
```

### Explanation of Changes:

1. **Asyncio Imports**: Added the necessary `asyncio` and `aiofiles` imports.
2. **Async Methods**: Changed the `load_assistant` method to be asynchronous (`async def load_assistant(self, name):`) and used `await` to open the file asynchronously.
3. **Main Method**: Created a new `main` method that is asynchronous (`async def main(self):`). This method gathers all the tasks to load assistants and runs them concurrently using `asyncio.gather(*tasks)`.
4. **Run Application**: The `main` method also handles the application run, making sure it is done within the asyncio context.
5. **Entry Point**: The entry point now uses `asyncio.run(App().main())` to run the main method asynchronously.

Make sure that the `MainWindow` and `Assistant` classes are capable of handling asynchronous operations. If they are not, you may need to refactor them accordingly.<|im_end|>

"""