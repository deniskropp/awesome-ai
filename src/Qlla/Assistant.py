class Assistant:
    def __init__(self, name, description, model):
        self.name = name
        self.description = description
        self.model = model

        with open(f"./{name}/prompt/System Instructions.txt", 'r') as f:
            self.prompt = f.read()
