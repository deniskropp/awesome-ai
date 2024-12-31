#!/usr/bin/env python3
import os
import argparse
import ollama

num_threads = int(os.environ.get('NUM_THREADS', -1))


# Main function to describe an image
def main(model, image, prompt, temp):
    response = ollama.chat(
        model=model,
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [image]
        }],
        options=ollama.Options(
            num_threads=num_threads,
            temperature=temp
        ),
        stream=True
    )

    for chunk in response:
        print(chunk['message']['content'], end='', flush=True)


# Run the main function if this script is executed directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Describe an image.')

    parser.add_argument('--image', type=str, default=None, help='Path to the input image')
    parser.add_argument('--prompt', type=str, default='What is in this image?', help='Content of the prompt')
    parser.add_argument('--model', type=str, default='llava-phi3', help='Name of the vision model')
    parser.add_argument('--temp', type=float, default=0.1, help='Temperature for the model')

    args = parser.parse_args()

    main(args.model, args.image, args.prompt, args.temp)
