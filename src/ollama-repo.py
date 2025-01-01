#!/usr/bin/env python

import ollama
import argparse

def run():
    # Getting the target file name (last argument)
    parser = argparse.ArgumentParser(description='Your script description')
    parser.add_argument('--model', type=str, default='qwen2.5-coder:7b', help='Model name')
    parser.add_argument('--repo', type=str, default='awesome-ai', help='Repository name')
    parser.add_argument('--prompt', type=str, help='Prompt for the model')
    parser.add_argument('files', nargs='+', help='List of files')
    args = parser.parse_args()

    repo_name = args.repo
    file_names = args.files[:-1]
    target_file_name = args.files[-1]

    prompt = f"{args.prompt}"
    print(prompt)

    prompt += f"<|repo_name|>{repo_name}\n"

    for file_name in file_names:
        try:
            with open(file_name, 'r') as file:
                content = file.read()
                prompt += f"<|file_sep|>{file_name}\n"
                prompt += f"{content}\n"
            print(f"⫻context/file:{file_name} ({len(content)})")
        except FileNotFoundError:
            print(f"File not found: {file_name}")

    prompt += f"<|file_sep|>{target_file_name}\n"
    print(f"⫻content/file:{target_file_name}")

    response = ollama.generate(args.model, prompt, raw=True, stream=True, options={
        "num_ctx": 4000,
        "num_predict": 4000,
        "num_thread": 6,
        "temperature": 0.1,
    })

    for part in response:
        print(part['response'], end='', flush=True)

    print('')


if __name__ == "__main__":
    run()
