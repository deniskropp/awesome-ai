#!/usr/bin/env python

import argparse
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

def run(args):
    repo_name = args.repo
    file_names = args.files[:-1]
    target_file_name = args.files[-1]

    prompt = f"{args.prompt}\n"

    prompt += f"<reponame>{repo_name}\n"

    print(prompt, end='')

    for file_name in file_names:
        try:
            with open(file_name, 'r') as file:
                content = file.read()
                prompt += f"<filename>{file_name}\n"
                prompt += f"{content}\n"
            print(f"⫻context/file:{file_name} ({len(content)})")
        except FileNotFoundError:
            print(f"File not found: {file_name}")

    prompt += f"<filename>{target_file_name}\n"
    print(f"⫻content/file:{target_file_name}")

    response = client.text_generation(
        model=args.model,
        prompt=prompt,
        stream=True,
        max_new_tokens=4000,
        temperature=0.1
    )

    for part in response:
        print(part, end='', flush=True)

    print('')


if __name__ == "__main__":
    # Getting the target file name (last argument)
    parser = argparse.ArgumentParser(description='Your script description')
    parser.add_argument('--model', type=str, default='Qwen/Qwen2.5-Coder-32B-Instruct', help='Model name')
    parser.add_argument('--repo', type=str, default='awesome-ai', help='Repository name')
    parser.add_argument('--prompt', type=str, help='Prompt for the model')
    parser.add_argument('files', nargs='+', help='List of files')
    args = parser.parse_args()

    run(args)
