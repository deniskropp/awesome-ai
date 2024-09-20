import ollama


import requests
import json



class Qllama(ollama.Client):
    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "qwen2:0.5b"):
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
        return res

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
        print(f"~response: {res['response']}")
        return res

    def generate_from_messages2(self, messages: list, system: str = "", options: dict = None) -> str:
        url = "https://api.fireworks.ai/inference/v1/chat/completions"
        payload = {
            "model": "accounts/fireworks/models/llama-v3p1-405b-instruct",
            "max_tokens": 16384,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.6,
            "messages": [
                {
                    "role": "system",
                    "content": system
                },
                *messages
            ]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer fw_3ZNpuVT55AYoXU4B5D1DxNTc"
        }
        res = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        return res.json()['choices'][0]['message']['content']


        print('\n\n\n--~~\n')
        print(f"~model: {self.model}")
        print(f"~options: {options}")
        print(f"~messages: {messages}")
        prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system}<|eot_id|>\n\n\n"
        for message in messages:
            prompt += f"<|start_header_id|>⫻{message.role}<|end_header_id|>\n{message.content}<|eot_id|>\n\n\n"
        print(f"~prompt:\n\"\"\"{prompt}\"\"\"\n\n\n")
        res = super().generate(
            model=self.model,
            prompt=prompt,
            raw=True,
            options=options
        )
        print(f"~response: {res['response']}")
        return res

    def generate_405(self, prompt: str = "", options: dict = None) -> str:
        url = "https://api.fireworks.ai/inference/v1/chat/completions"
        payload = {
            "model": "accounts/fireworks/models/llama-v3p1-405b-instruct",
            "max_tokens": 16384,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.6,
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer fw_3ZNpuVT55AYoXU4B5D1DxNTc"
        }
        res = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        return res.json()['choices'][0]['message']['content']


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
