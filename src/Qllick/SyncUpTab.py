from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton, QTextEdit , QFormLayout, QListWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown
from .qllama import Registry  # Assuming qllama is a module for AI registry and communication


registry = Registry()


class SyncUpTab(QWidget):
    """
        Title: Qt5 Implementation of SIN's SyncUp UI

        **1. Class Definition:**

        - Define a `SyncUpTab` class that inherits from `QWidget`. This class will serve as the main container for the SyncUp UI.

        **2. UI Components:**

        - **Project Goal and Parameter Setting:**
            - Use `QFormLayout` or `QGridLayout` to create a section for setting project goals and parameters.
            - Include `QLineEdit`, `QComboBox`, and `QSpinBox` widgets for inputting text, selecting options, and adjusting numerical values, respectively.
        - **Task Management:**
            - Implement a `QListWidget` or `QTableWidget` to display tasks and their status.
            - Include buttons for adding, removing, and prioritising tasks.
        - **Communication and Feedback:**
            - Use `QTextEdit` or `QLabel` widgets to display AI-generated outputs in a human-readable format.
            - Incorporate visualisation tools like `QChartView` or `PyQtGraph` to present data and insights.
            - Implement a section for users to input feedback and instructions for the AI.
        - **User Control and Intervention:**
            - Include buttons or checkboxes for users to manually intervene in the AI's operation when necessary.
            - Implement a section for users to provide direct instructions to specific AI agents or spokes within Neural Nexus.

        **3. Functionality:**

        - **Task Delegation and Management:**
            - Implement methods for adding, removing, and prioritising tasks.
            - When a task is added, delegate it to the appropriate "spoke" within Neural Nexus based on the task's nature and the specialisation of the AI agents.
        - **Communication and Feedback:**
            - Implement methods for receiving and displaying AI-generated outputs.
            - Incorporate Explainable AI (XAI) features to provide clear explanations for AI decisions and recommendations.
        - **User Control and Intervention:**
            - Implement methods for users to manually intervene in the AI's operation when necessary.
            - Provide options for users to provide direct instructions to specific AI agents or spokes within Neural Nexus.

        **4. Integration with Neural Nexus:**

        - Establish a communication protocol between SyncUpTab and Neural Nexus to enable the exchange of data and instructions.
        - Implement methods for sending tasks and user feedback to Neural Nexus and receiving AI-generated outputs.

        **5. User-Centric Design and Accessibility:**

        - Design the UI with user-centric design principles in mind, ensuring it is intuitive, easy to navigate, and tailored to the specific needs of the target user group.
        - Incorporate accessibility features to ensure the UI is usable by users with diverse abilities and needs.

        **6. Security and Data Privacy:**

        - Implement robust security measures to protect user data.
        - Ensure the privacy of user data by adhering to data protection regulations and best practices.
    """
    def __init__(self, parent=None):
        super(SyncUpTab, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

        # Project Goal and Parameter Setting
        form_layout = QFormLayout()
        
        # Project Name
        self.project_name = QLineEdit()
        form_layout.addRow(QLabel("Project Name:"), self.project_name)
        
        # Project Goal
        self.project_goal = QTextEdit()
        form_layout.addRow(QLabel("Project Goal:"), self.project_goal)
        
        # Parameters (example: threshold, data source)
        self.threshold = QSpinBox()
        self.threshold.setRange(0, 100)
        form_layout.addRow(QLabel("Threshold:"), self.threshold)
        
        # Data Source
        self.data_source = QComboBox()
        self.data_source.addItems(["Source 1", "Source 2", "Source 3"])
        form_layout.addRow(QLabel("Data Source:"), self.data_source)
        
        layout.addLayout(form_layout)

        # Task Management
        task_layout = QVBoxLayout()
        
        # Task List
        self.task_list = QListWidget()
        task_layout.addWidget(QLabel("Tasks:"))
        task_layout.addWidget(self.task_list)
        
        # Task Management Buttons
        self.add_task_button = QPushButton("Add Task")
        self.remove_task_button = QPushButton("Remove Task")
        self.priority_task_button = QPushButton("Prioritize Task")
        
        task_layout.addWidget(self.add_task_button)
        task_layout.addWidget(self.remove_task_button)
        task_layout.addWidget(self.priority_task_button)
        
        layout.addLayout(task_layout)

        # Communication and Feedback
        feedback_layout = QVBoxLayout()
        
        # AI Output
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        feedback_layout.addWidget(QLabel("AI Output:"))
        feedback_layout.addWidget(self.ai_output)
        
        # User Feedback
        self.user_feedback = QTextEdit()
        self.send_feedback_button = QPushButton("Send Feedback")
        
        feedback_layout.addWidget(QLabel("User Feedback:"))
        feedback_layout.addWidget(self.user_feedback)
        feedback_layout.addWidget(self.send_feedback_button)
        
        layout.addLayout(feedback_layout)

        # User Control and Intervention
        control_layout = QVBoxLayout()
        
        # Manual Intervention
        self.intervene_button = QPushButton("Intervene")
        self.intervene_button.setCheckable(True)
        
        # Direct Instructions
        self.direct_instructions = QTextEdit()
        self.send_instructions_button = QPushButton("Send Instructions")
        
        control_layout.addWidget(QLabel("Manual Intervention:"))
        control_layout.addWidget(self.intervene_button)
        
        control_layout.addWidget(QLabel("Direct Instructions:"))
        control_layout.addWidget(self.direct_instructions)
        control_layout.addWidget(self.send_instructions_button)
        
        layout.addLayout(control_layout)

        # Set the main layout
        self.setLayout(layout)

        # Connect signals to slots
        self.add_task_button.clicked.connect(self.add_task)
        self.remove_task_button.clicked.connect(self.remove_task)
        self.priority_task_button.clicked.connect(self.priority_task)
        self.send_feedback_button.clicked.connect(self.send_feedback)
        self.intervene_button.clicked.connect(self.intervene)
        self.send_instructions_button.clicked.connect(self.send_instructions)

    def add_task(self):
        task_name, ok = 'unnamed', True #QInputDialog.getText(self, "Add Task", "Enter Task Name:")
        if ok and task_name:
            self.task_list.addItem(task_name)
            # Delegate task to Neural Nexus
            self.delegate_task(task_name)

    def remove_task(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.task_list.takeItem(self.task_list.row(item))

    def priority_task(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                # Move item to the top of the list
                self.task_list.takeItem(self.task_list.row(item))
                self.task_list.insertItem(0, item)

    def delegate_task(self, task_name):
        # Example: Send task to Neural Nexus
        Registry.delegate_task(task_name, self.data_source.currentText())

    def receive_output(self, output):
        # Example: Update the AI output display
        self.ai_output.setHtml(markdown(output))

    def send_feedback(self):
        feedback = self.user_feedback.toPlainText()
        if feedback:
            # Example: Send feedback to Neural Nexus
            Registry.send_feedback(feedback)
            self.user_feedback.clear()

    def intervene(self):
        if self.intervene_button.isChecked():
            # Example: Notify Neural Nexus of manual intervention
            Registry.notify_intervention()
        else:
            # Example: Notify Neural Nexus to resume automated operation
            Registry.notify_resume()

    def send_instructions(self):
        instructions = self.direct_instructions.toPlainText()
        if instructions:
            # Example: Send direct instructions to specific AI agents
            Registry.send_instructions(instructions)
            self.direct_instructions.clear()
