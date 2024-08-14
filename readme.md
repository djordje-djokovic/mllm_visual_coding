# Visual coding using multi-modal large language models (ChatGPT-4o) in social sciences.


Images and videos provide information that text alone often misses, presenting both opportunities for richer analysis and challenges in scaling and integrating these insights for social scientists. Traditional visual coding is labor-intensive, requiring trained coders to analyze data manually. This study investigates the potential of multimodal large language models (MLLMs), specifically ChatGPT-4o, released in May 2024, for handling complex visual coding tasks in social sciences. 

## Installation

To get started with the project, first, navigate to the `mllm_visual_coding` directory and install the required dependencies using `pip`. You can do this by following these steps:

```bash
cd mllm_visual_coding
pip install -r requirements.txt
```

## Running the Script

You can run the script from the `mllm_visual_coding/mllm_visual_coding` directory to work with relative paths. Below is an example command:

```bash
cd mllm_visual_coding/mllm_visual_coding
python your_script.py --temperature 0.5 --image_folder "img" --output_path "results.json" --prompt_file "prompt.txt" --force
```

### Arguments

- **`--temperature`**: Controls the randomness of the process. Lower values mean less randomness. Default is `0.2`.
- **`--image_folder`**: The folder containing the input images. This is where all images in the folder will be read and processed. Default is `img`.
- **`--output_path`**: Path to save the output JSON file containing the results of the processing, such as annotations or predictions. If not provided, a default file named `output_{T=<temperature>}.json` will be created.
- **`--vlm_prompt`**: Optional prompt or command used by the Vision Language Model (VLM) during processing. This can be overridden by `--prompt_file`.
- **`--prompt_file`**: Path to a text file containing the prompt. If provided, this will override the `--vlm_prompt` argument.
- **`--force`**: If set, this flag will force the script to overwrite existing files or perform actions that are otherwise skipped.

### Prompt Configuration

You can change the prompt by using the `--vlm_prompt` argument directly or by pointing to a different prompt file using the `--prompt_file` argument. If both are provided, the `--prompt_file` will take precedence.

### Force Flag

If the `--force` flag is not set, the script will attempt to resume from the last point if the output file already exists. Results are persisted to the specified output file, and the script can recover from the last point if it is interrupted.

### Image Processing

All images in the `img` folder or any other folder specified in the `--image_folder` argument will be read and processed. Make sure your images are placed in the correct directory.

### .env File Configuration

The `.env` file should be placed in the `mllm_visual_coding` directory (not in `mllm_visual_coding/mllm_visual_coding`). This file is required immediately after installation to configure the environment.

The `.env` file should look like this:

```bash
OPENAI_API_KEY='sk-yourapikeyhere'
```

Replace `'sk-yourapikeyhere'` with your actual OpenAI API key.

### Obtaining an OpenAI API Key

To obtain an OpenAI API key, sign up for an account on [OpenAI's website](https://beta.openai.com/signup/) and navigate to the API section. Once you've generated your API key, add it to your `.env` file as shown above.
