import re, os, json, requests, openai, tqdm, base64
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv("..\\.env")

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to query the model with an image and a prompt
def query_image(image_path, prompt, max_attempts=3, temperature=0):
    # Encode the image in base64
    base64_image = encode_image(image_path)

    # Add instruction to ensure JSON output
    prompt_with_json_instruction = prompt
    # prompt_with_json_instruction = f"""
    # {prompt}
    #
    # Ensure the output is a valid JSON object and avoid including any additional text or explanation. Just return the JSON.
    # """

    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    for attempt in range(max_attempts):
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_with_json_instruction
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high",
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 2000,
            "temperature": temperature
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_json = response.json()

        if response.status_code == 200:
            response_text = response_json['choices'][0]['message']['content'].strip()
            try:
                response_json = extract_json(response_text)
                return response_json  # Return the JSON if parsing is successful
            except Exception as error:
                print(f"Attempt {attempt + 1}: Failed to parse JSON response. {str(error)}")
        else:
            print(f"Error: {response_json}")

    print(f"Failed to get a valid JSON response after {max_attempts} attempts.")
    return None

# Main function to process images based on the survey
def query_images(image_folder, output_path, vlm_prompt, temperature=0, force=False):
    if force and os.path.exists(output_path):
        os.remove(output_path)

    results = []

    if not force and os.path.exists(output_path):
        with open(output_path, 'r') as file:
            results = json.load(file)
        last_index = results[-1]['Index']
        start_index = last_index + 1
    else:
        start_index = 1

    # Get a list of all image paths in the directory
    # You can adjust the glob pattern to match the file extensions you're interested in (e.g., '*.jpg', '*.png')
    image_extensions = ["*.jpg", "*.png", "*.jpeg"]  # Add other extensions as needed

    data = []
    for ext in image_extensions:
        data.extend(image_folder.glob(ext))  # Add all images matching the extension to the list

    # Use tqdm for progress tracking

    with tqdm(total=len(data[start_index - 1:]), desc="Processing Images") as pbar:
        index = 0
        for image_path in data[start_index - 1:]:
            result = query_image(str(image_path), vlm_prompt, 3, temperature)
            if result:
                result_dict = {
                    "Index": index,
                    "Image": str(image_path),
                    **result
                }
                results.append(result_dict)

                # Save intermediate results
                with open(output_path, 'w') as file:
                    json.dump(results, file, indent=4)
                index += 1
            pbar.update(1)

# Function to extract JSON from text
def extract_json(response_text):
    try:
        # Use regex to find JSON object in the text
        json_pattern = re.compile(r'(\{.*\})', re.DOTALL)
        match = json_pattern.search(response_text)
        if match:
            return json.loads(match.group(1))
        else:
            raise ValueError("No JSON object found in the response text")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

def count_tokens(str_prompt):
    # Tokenize the string
    # Tokenize the string using the updated API structure
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": str_prompt
            }
        ],
        max_tokens=1  # Only interested in tokenizing the input
    )
    return response.usage.total_tokens

