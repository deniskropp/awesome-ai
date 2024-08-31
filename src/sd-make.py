import argparse
import csv
import datetime
import json
import os
import yaml

#import matplotlib.pyplot as plt
from PIL import Image

from diffusers import StableDiffusionPipeline
import torch

### [(lora['name'], lora['scale']) for lora in args['loras']]

def load_args_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
        if ('loras' in data):
            data['lora'] = data['loras']
            data['loras'] = None
        return data



class StableDiffusionGenerator:
    device: str
    pipe: StableDiffusionPipeline
    model: str
    loras: list[str]
    adapter_names: list[str]
    adapter_weights: list[float]
    generator: torch.Generator

    def __init__(self, model_id):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using {self.device} device")

        if (os.path.isfile(model_id)):
            self.pipe = StableDiffusionPipeline.from_single_file(model_id, torch_dtype=torch.float16)
        else:
            self.pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        self.pipe = self.pipe.to(self.device)

        self.model = model_id
        self.loras = []
        self.adapter_names = []
        self.adapter_weights = []

    def load_lora_weights(self, lora, scale=1.0):
        #assert(self.generator is None)
        print('Loading', lora, scale)
        self.loras.append(lora)
        self.pipe.load_lora_weights(".", weight_name=lora)
        for l in self.pipe.get_active_adapters():
            self.adapter_names.append(l)
            self.adapter_weights.append(scale)

    def fuse(self, lora_scale=0.5):
        #assert(self.generator is None)
        print('fusing', self.adapter_names, self.adapter_weights)
        if (len(self.adapter_names) != 0):
            self.pipe.set_adapters(self.adapter_names, adapter_weights=self.adapter_weights)
            self.pipe.fuse_lora(lora_scale=lora_scale, adapter_names=self.adapter_names)
            self.pipe.unload_lora_weights()
        self.generator = torch.Generator(device=self.device)

    def generate_image(self, prompt, width, height, num_inference_steps, guidance_scale) -> Image:
        #assert(self.generator is not None)
        return self.pipe(
            prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=self.generator
        ).images[0]

    def save_image_and_info(self, image, output_path_noext, timestamp, seed,
                            prompt, width, height, num_inference_steps, guidance_scale):
        # Save the image content (png)
        image.save(f"{output_path_noext}_{timestamp}.png")

        # Save the image information (yaml)
        image_info = {
            'model': self.model,
            'lora': self.loras,
            'prompt': prompt,
            'width': width,
            'height': height,
            'num_inference_steps': num_inference_steps,
            'guidance_scale': guidance_scale,
            'timestamp': timestamp,
            'seed': seed,
        }
        with open(f"{output_path_noext}_{timestamp}.yaml", 'w') as file:
            yaml.dump(image_info, file)


    def prepare(self, seed):
        #assert(self.generator is not None)
        if seed is None:
            seed = self.generator.seed()
        else:
            self.generator = self.generator.manual_seed(seed)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return seed, timestamp

    def run(self, seed, timestamp, output, prompt, width, height, num_inference_steps, guidance_scale):
        image = self.generate_image(prompt, width, height, num_inference_steps, guidance_scale)
        self.save_image_and_info(image, f"{output}/sd_", timestamp, seed,
                                 prompt, width, height, num_inference_steps, guidance_scale)
        return image


def main():
    """
        SD Make

        Main function to run the Stable Diffusion image generation.

            1. Parse the command-line arguments.
            2. Create an instance of the StableDiffusionGenerator class.
            3. Load the LoRA weights if provided.
            4. Run the image generation and save the results.
            5. Print the seed for each generated image.
            6. Print the output path for each generated image.
            7. Print the timestamp for each generated image.

            8. TODO: Add support for multiple LoRA models.
            9. TODO: Add support for multiple prompts.
            10. TODO: Add support for multiple seeds.
            11. TODO: Add support for multiple widths and heights.
            12. TODO: Add support for multiple num_inference_steps.
            13. TODO: Add support for multiple guidance_scales.
            14. TODO: Add support for multiple output paths.
            15. TODO: Add support for multiple devices.
            16. TODO: Add support for multiple models.
            17. TODO: Add support for multiple count.
            18. TODO: Add support for multiple seeds.
            19. TODO: Add support for multiple prompts.
            20. TODO: Add support for multiple widths and heights.
            21. TODO: Add support for multiple num_inference_steps.
            22. TODO: Add support for multiple guidance_scales.


            TODO: Instead of bumping up the seed, the following should be possible:
                    args.num_inference_steps += 5   OR
                    args.guidance_scale += 0.2
    """
    parser = argparse.ArgumentParser(description='Generate an image using Stable Diffusion and a LoRA model.')
    parser.add_argument('--count', type=int, default=1, help='Number of images to generate')
    parser.add_argument('--output', type=str, default='sd-output', help='Output path to save the images content and information')
    parser.add_argument('--model', type=str, default=None, help='Path to the base model')
    parser.add_argument('--prompt', type=str, default=None, help='The prompt for image generation')
    parser.add_argument('--lora', action='append', help='Path to the LoRA model')
    parser.add_argument('--lora_scale', type=float, default=None, help='Weight applied with fused loras at the output')
    parser.add_argument('--seed', type=int, default=None, help='Seed for random number generation')
    parser.add_argument('--width', type=int, default=None, help='Width of the output image')
    parser.add_argument('--height', type=int, default=None, help='Height of the output image')
    parser.add_argument('--num_inference_steps', type=int, default=None, help='Number of denoising steps')
    parser.add_argument('--guidance_scale', type=float, default=None, help='Guidance scale for classifier-free guidance')
    parser.add_argument('--yaml', type=str, default=None, help='Load parameters from YAML (args or sd_)')
    yaml_args = parser.parse_args()

    print('\nyaml_args', yaml_args)

    yaml_args.lora = []

    # If a YAML file is provided, load the parameters from it
    # The command line arguments will override the YAML file arguments
    if yaml_args.yaml:
        yaml_data = load_args_from_yaml(yaml_args.yaml)
        yaml_args.__dict__.update(yaml_data)

    print('\nyaml_args', yaml_args)

    args = parser.parse_args()

    print('\n\nargs', args)

    if args.model is None:
        args.model = yaml_args.model if yaml_args.model else 'stable-diffusion/v1-5'

    if args.prompt is None:
        args.prompt = yaml_args.prompt if yaml_args.prompt else 'a kinky hood in the forest'

    if args.lora is None:
        args.lora = []

    if yaml_args.lora:
        args.lora.extend(yaml_args.lora)

    if args.lora_scale is None:
        args.loras_scale = yaml_args.lora_scale if yaml_args.lora_scale else 1.0

    if args.seed is None:
        args.seed = yaml_args.seed if yaml_args.seed else None

    if args.width is None:
        args.width = yaml_args.width if yaml_args.width else 512

    if args.height is None:
        args.height = yaml_args.height if yaml_args.height else 512

    if args.num_inference_steps is None:
        args.num_inference_steps = yaml_args.num_inference_steps if yaml_args.num_inference_steps else 20

    if args.guidance_scale is None:
        args.guidance_scale = yaml_args.guidance_scale if yaml_args.guidance_scale else 7.5

    print('\n\nargs', args)

    # Create output directory if it does not exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Save the arguments to a JSON file
    with open(os.path.join(args.output, f"args.json"), "w") as f:
        json.dump(vars(args), f, indent=4)

    # Save the arguments to a CSV file
    with open(os.path.join(args.output, "args.csv"), "a") as f:
        writer = csv.writer(f)
        writer.writerow(vars(args).keys())
        writer.writerow(vars(args).values())

    # Save the arguments to a TXT file
    with open(os.path.join(args.output, "args.txt"), "a") as f:
        f.write(str(vars(args)) + "\n")

    # Save the arguments to a YAML file
    with open(os.path.join(args.output, f"args.yaml"), "w") as f:
        yaml.dump(vars(args), f)

    # Use the provided model path if available, otherwise use the default path
    model_path = args.model if args.model else "./stable-diffusion/sd-v1-5.safetensors"

    # Initialize the StableDiffusionGenerator with the model path
    generator = StableDiffusionGenerator(model_path)

    # Load LoRA weights if provided
    for lora in args.lora:
        # Extract filename and scale from lora
        lora_info = lora.split(':')
        lora_filename = lora_info[0]
        lora_scale = float(lora_info[1]) if len(lora_info) > 1 else 1.0

        # Load LoRA weights with the extracted scale
        generator.load_lora_weights(lora_filename, lora_scale)

    # Fuse the LoRA weights into the base model
    generator.fuse(lora_scale=args.lora_scale if args.lora_scale is not None else 1.0)

    # Generate images based on the specified count
    for i in range(args.count):
        # Make a timestamp and update the seed
        seed, timestamp = generator.prepare(args.seed)

        # Print a newline for better readability
        print('\n----\n')
        # Print the current date and time
        print(f"Date and time: {datetime.datetime.now()}")
        # Print the seed for each generated image
        print(f"Seed: {args.seed}")
        # Print the size of each generated image
        print(f"Size: {args.width}x{args.height}")
        # Print the base model used for each generated image
        print(f"Model: {model_path}")
        # Print the prompt for each generated image
        print(f"Prompt: {args.prompt}")
        # Print the number of denoising steps for each generated image
        print(f"Steps: {args.num_inference_steps}")
        # Print the guidance scale for each generated image
        print(f"Guidance Scale: {args.guidance_scale}")
        # Print the LoRA models used for each generated image
        print(f"LoRA models: {args.lora}")
        # Print the LoRA scale used for each generated image
        print(f"LoRA scale: {args.lora_scale}")
        # Print the seed for each generated image
        print(f"Seed: {seed}")
        # Print the timestamp for each generated image
        print(f"Timestamp: {timestamp}")
        # Print the output path for each generated image
        print(f"Output: {args.output}")
        # Print the current iteration
        print(f"---- {i+1}/{args.count}\n")

        image = generator.run(seed, timestamp, args.output, args.prompt, args.width, args.height, args.num_inference_steps, args.guidance_scale)

        # Increment the seed for the next iteration if it's not None
        if args.seed is not None:
            args.seed+=1

        # Display the image
        #plt.imshow(image)
        #plt.axis('off')
        #plt.show()


# Run the main function
if __name__ == "__main__":
    main()