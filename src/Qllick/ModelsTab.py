from PyQt5 import QtCore, QtWidgets
from Qllick.qllama import Registry


# Create a singleton instance of QllamaRegistry
registry = Registry()


class ModelsTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
    
        # List the available models
        self.models = registry.list_models()
        self.models.sort()

        # Create a table to display the available models
        self.models_table = QtWidgets.QTableWidget()
        self.models_table.setColumnCount(2)
        self.models_table.setHorizontalHeaderLabels(["Name", "Size"])
        self.models_table.setColumnWidth(0, 400)
        self.models_table.setColumnWidth(1, 70)
        self.models_table.setRowCount(len(self.models))

        # Populate the table with model data
        for i, model in enumerate(self.models):
            m = registry.get_model(model)
            self.models_table.setItem(i, 0, QtWidgets.QTableWidgetItem(m.name))
            # Convert size from bytes to gigabytes and round to 2 decimal places
            size = round(m.size / (1024 ** 3), 2)
            self.models_table.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{size} GB"))
            # Store the model data in the table item for later use
            self.models_table.item(i, 0).setData(QtCore.Qt.UserRole, m)

        # Add a list item handler to the model_list table
        self.models_table.itemClicked.connect(self.load_model)

        # Add spacing/separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Add model specs like template, system prompt
        self.model_specs = QtWidgets.QTableWidget()
        self.model_specs.setColumnCount(2)
        self.model_specs.setHorizontalHeaderLabels(["Parameter", "Value"])
        self.model_specs.setColumnWidth(0, 200)
        self.model_specs.setColumnWidth(1, 400)
        self.model_specs.setRowCount(2)  # Assuming there are 2 specs to display

        # Populate the table with model spec data
        self.model_specs.setItem(0, 0, QtWidgets.QTableWidgetItem("Template"))
        #self.model_specs.setItem(0, 1, QtWidgets.QTableWidgetItem(model['template']))  # Replace 'template' with the actual key in the model dictionary
        self.model_specs.setItem(1, 0, QtWidgets.QTableWidgetItem("System Prompt"))
        #self.model_specs.setItem(1, 1, QtWidgets.QTableWidgetItem(model['system_prompt']))  # Replace 'system_prompt' with the actual key in the model dictionary

        # Create a layout for the tab
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.models_table)
        layout.addWidget(separator)
        layout.addWidget(self.model_specs)

        self.setLayout(layout)

    # Load a model from the models tab
    def load_model(self, item):
        # Get the model name from the selected item
        m = self.models_table.item(item.row(), 0).data(QtCore.Qt.UserRole)
        self.model_specs.setItem(0, 1, QtWidgets.QTableWidgetItem(m.template))  # Replace 'template' with the actual key in the model dictionary
        self.model_specs.setItem(1, 1, QtWidgets.QTableWidgetItem(m.system_prompt))  # Replace 'system_prompt' with the actual key in the model dictionary
