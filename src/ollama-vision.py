#!/usr/bin/env python3
import os
import sys
import argparse
import ollama
from typing import Optional, List
from pathlib import Path

class ImageProcessor:
    def __init__(self, model: str, temperature: float, num_threads: int):
        self.model = model
        self.temperature = temperature
        self.num_threads = num_threads

    def process_images(self, images: List[str], prompt: str, output_file: Optional[str] = None):
        """Process multiple images with the same prompt"""
        if not images:
            print("Error: No images provided", file=sys.stderr)
            return

        # Validate all images exist before processing
        for img_path in images:
            if not os.path.exists(img_path):
                print(f"Error: Image not found: {img_path}", file=sys.stderr)
                return

        responses = []
        for img_path in images:
            print(f"\nProcessing image: {img_path}", file=sys.stderr)
            response = self._process_single_image(img_path, prompt)
            responses.append({"image": img_path, "response": response})

        if output_file:
            self._save_responses(responses, output_file)
        else:
            self._print_responses(responses)

    def _process_single_image(self, image_path: str, prompt: str) -> str:
        """Process a single image and return the response"""
        response_text = ""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [image_path]
                }],
                options=ollama.Options(
                    num_threads=self.num_threads,
                    temperature=self.temperature
                ),
                stream=True
            )

            for chunk in response:
                content = chunk['message']['content']
                response_text += content
                if not self.quiet:
                    print(content, end='', flush=True)

            return response_text.strip()

        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}", file=sys.stderr)
            return ""

    def _save_responses(self, responses: List[dict], output_file: str):
        """Save responses to a file"""
        with open(output_file, 'w') as f:
            for resp in responses:
                f.write(f"Image: {resp['image']}\n")
                f.write(f"Response: {resp['response']}\n")
                f.write("-" * 80 + "\n")

    def _print_responses(self, responses: List[dict]):
        """Print responses to stdout"""
        for resp in responses:
            print(f"\nImage: {resp['image']}")
            print(f"Response: {resp['response']}")
            print("-" * 80)

def main():
    parser = argparse.ArgumentParser(description='Advanced CLI for image-to-text processing using Ollama.')

    parser.add_argument('images', nargs='+', help='Path(s) to input image(s)')
    parser.add_argument('--prompt', '-p', type=str, default='What is in this image?', help='Content of the prompt')
    parser.add_argument('--model', '-m', type=str, default='llava-phi3', help='Name of the vision model')
    parser.add_argument('--temp', '-t', type=float, default=0.1, help='Temperature for the model (0.0 to 1.0)')
    parser.add_argument('--output', '-o', type=str, help='Output file to save responses')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress streaming output')
    parser.add_argument('--threads', '-T', type=int, default=os.environ.get('NUM_THREADS'), help='Number of threads to use')

    args = parser.parse_args()

    # Input validation
    if args.temp < 0 or args.temp > 2:
        print("Error: Temperature must be between 0.0 and 2.0", file=sys.stderr)
        sys.exit(1)

    processor = ImageProcessor(
        model=args.model,
        temperature=args.temp,
        num_threads=args.threads
    )
    processor.quiet = args.quiet
    processor.process_images(args.images, args.prompt, args.output)

if __name__ == "__main__":
    main()
