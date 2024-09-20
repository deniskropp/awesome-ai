import ollama


class Qllama(ollama.Client):
    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "qwen2.5:0.5b"):
        # Initialize the Ollama class with the base URL
        super().__init__(base_url)
        # Set the default model
        self.model = model

    def list(self) -> list:
        return super().list()['models']

    def generate(self, prompt: str, system: str = "", options: dict = None) -> str:
        print('\n\n\n--~~\n')
        print(f"~model: {self.model}")
        print(f"~options: {options}")
        print(f"~system: {system}")
        print(f"~prompt: {prompt}")
        res = super().generate(model=self.model, prompt=prompt, system=system, options=options)
        print(f"~response: {res['response']}")
        return res['response']

    def chat(self, messages: list, system: str = "", options: dict = None) -> str:
        print('\n\n\n--~~\n')
        print(f"~model: {self.model}")
        print(f"~options: {options}")
        print(f"~system: {system}")
        print(f"~messages: {messages}")
        messages = [
                {
                    "role": "system",
                    "content": system
                },
                *messages
        ]
        res = super().chat(model=self.model, messages=messages, options=options)
        print(f"~response: {res['message']['content']}")
        return res['message']['content']


    def generate_raw(self, prompt: str = "", options: dict = None) -> str:
        print('\n\n\n--~~\n')
        print(f"~model: {self.model}")
        print(f"~options: {options}")
        print(f"~prompt:\n\"\"\"{prompt}\"\"\"\n\n\n")
        res = super().generate(
            model=self.model,
            prompt=prompt,
            raw=True,
            options=options
        )
        print(f"~response: {res['response']}")
        return res['response']
