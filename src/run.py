import os
from typing import List
# from ollama import generate
from openai import OpenAI


with open('./MultiMax/prompt/System Instructions.txt', 'r') as f:
    system_prompt = f.read()

print(system_prompt)


# options = {
#    'temperature': 0.7,
#    'num_gpu': 1
# }


def make_prompt(input: List[str], output: str):
    prompt = ""

    for i, file in enumerate(input):
        with open(file, 'r') as f:
            prompt += f"⫻context:{file}\n{f.read()}\n\n\n"
    
    prompt += f"⫻content:{output}"

    #print(prompt)
    
    return prompt


# prompt = make_prompt(["src/Entity.hpp", "src/World.hpp"], "src/World.cpp")

prompt = 'Explain your role'


# response = generate('codestral', system=system_prompt, prompt=prompt, options=options)
# print(response['response'])


client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=os.getenv("AIML_API_KEY"),
)

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": prompt
    },
]

response = client.chat.completions.create(
    #    model="Phind/Phind-CodeLlama-34B-v2",
    #    model="deepseek-ai/deepseek-coder-33b-instruct",
    # model="Qwen/Qwen2-72B-Instruct",
    model="meta-llama/Llama-3-70b-chat-hf",
    messages=messages,
)
print(response.choices[0].message.content)
