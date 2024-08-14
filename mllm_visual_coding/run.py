from common import query_images
import argparse
from pathlib import Path

# Function to load prompt from a text file
def load_prompt_from_file(prompt_file_path):
    with open(prompt_file_path, 'r') as file:
        return file.read().strip()

if __name__ == "__main__":
    # Create an ArgumentParser object to handle command-line arguments
    parser = argparse.ArgumentParser(description="Process some images and save results based on a temperature setting.")

    # Add arguments to the parser
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.2,
        help='Temperature parameter used in processing. It typically controls the randomness of the process, where lower values mean less randomness.'
    )

    parser.add_argument(
        '--image_folder',
        type=str,
        default=str('img'),
        help='Path to the folder containing input images. This folder is used to retrieve images for processing.'
    )

    parser.add_argument(
        '--output_path',
        type=str,
        default=None,
        help='Path to save the output JSON file. This file will contain the results of the processing, such as annotations or predictions.'
    )

    parser.add_argument(
        '--vlm_prompt',
        type=str,
        help='Optional prompt or command used by the Vision Language Model (VLM) during processing. This can be overridden by --prompt_file.'
    )

    parser.add_argument(
        '--prompt_file',
        type=str,
        help='Path to a text file containing the prompt. If provided, this will override the --vlm_prompt argument.'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='If set, this flag will force the script to overwrite existing files or perform actions that are otherwise skipped.'
    )

    # Parse the arguments provided by the user
    args = parser.parse_args()

    # Load the prompt from the file if provided
    if args.prompt_file:
        vlm_prompt = load_prompt_from_file(args.prompt_file)
    else:
        vlm_prompt = args.vlm_prompt

    # If the output_path is not provided, create a default one based on the temperature
    if args.output_path is None:
        args.output_path = f'output_{{T={args.temperature}}}.json'

    # Convert paths from strings to Path objects
    image_folder = Path(args.image_folder)
    output_path = Path(args.output_path)
    temperature = args.temperature
    force = args.force

    # Start of the processing using the provided arguments
    # Replace this with the actual processing logic you have
    print(f"Processing images from {image_folder}")
    print(f"Saving results to: {output_path}")
    print(f"Temperature setting: {args.temperature}")
    print(f"VLM Prompt: '{vlm_prompt}'")

    # vlm_prompt = "What do you see in the image. Describe it in detail"
    # count_tokens(str(vlm_prompt))
    query_images(image_folder, output_path, vlm_prompt, temperature=temperature, force=force)
