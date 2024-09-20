from PyQt5 import QtWidgets

class StableDiffusionTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Create controls for each argument
        self.count_spinbox = QtWidgets.QSpinBox()
        self.count_spinbox.setMinimum(1)
        self.count_spinbox.setMaximum(10)
        self.count_spinbox.setToolTip('Number of images to generate')

        self.output_lineedit = QtWidgets.QLineEdit('sd-output')
        self.output_lineedit.setToolTip('Output path to save the images content and information')

        self.model_lineedit = QtWidgets.QLineEdit()
        self.model_lineedit.setToolTip('Path to the base model')

        self.prompt_lineedit = QtWidgets.QLineEdit()
        self.prompt_lineedit.setToolTip('The prompt for image generation')

        self.lora_lineedit = QtWidgets.QLineEdit()
        self.lora_lineedit.setToolTip('Path to the LoRA model')

        self.lora_scale_spinbox = QtWidgets.QDoubleSpinBox()
        self.lora_scale_spinbox.setToolTip('Weight applied with fused loras at the output')

        self.seed_spinbox = QtWidgets.QSpinBox()
        self.seed_spinbox.setToolTip('Seed for random number generation')

        self.width_spinbox = QtWidgets.QSpinBox()
        self.width_spinbox.setMinimum(1)
        self.width_spinbox.setMaximum(4096)
        self.width_spinbox.setToolTip('Width of the output image')

        self.height_spinbox = QtWidgets.QSpinBox()
        self.height_spinbox.setMinimum(1)
        self.height_spinbox.setMaximum(4096)
        self.height_spinbox.setToolTip('Height of the output image')

        self.num_inference_steps_spinbox = QtWidgets.QSpinBox()
        self.num_inference_steps_spinbox.setMinimum(1)
        self.num_inference_steps_spinbox.setMaximum(1000)
        self.num_inference_steps_spinbox.setToolTip('Number of denoising steps')

        self.guidance_scale_spinbox = QtWidgets.QDoubleSpinBox()
        self.guidance_scale_spinbox.setToolTip('Guidance scale for classifier-free guidance')

        self.yaml_lineedit = QtWidgets.QLineEdit()
        self.yaml_lineedit.setToolTip('Load parameters from YAML (args or sd_)')

        # Create layout for controls
        layout = QtWidgets.QFormLayout()
        layout.addRow('Count:', self.count_spinbox)
        layout.addRow('Output:', self.output_lineedit)
        layout.addRow('Model:', self.model_lineedit)
        layout.addRow('Prompt:', self.prompt_lineedit)
        layout.addRow('LoRA:', self.lora_lineedit)
        layout.addRow('LoRA Scale:', self.lora_scale_spinbox)
        layout.addRow('Seed:', self.seed_spinbox)
        layout.addRow('Width:', self.width_spinbox)
        layout.addRow('Height:', self.height_spinbox)
        layout.addRow('Num Inference Steps:', self.num_inference_steps_spinbox)
        layout.addRow('Guidance Scale:', self.guidance_scale_spinbox)
        layout.addRow('YAML:', self.yaml_lineedit)

        self.setLayout(layout)
