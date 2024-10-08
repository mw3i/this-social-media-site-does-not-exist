import openai
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv('../env')

# Fetch OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the API key is available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Make sure it's in the .env file.")

# Function to send a prompt to the OpenAI ChatGPT model and return the text response
def chatgpt(prompt):
    # Use the OpenAI client as a context manager
    with openai.OpenAI(api_key=OPENAI_API_KEY) as client:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
        )
        return chat_completion.choices[0].message.content.strip()

def dalle(prompt):
    with openai.OpenAI(api_key=OPENAI_API_KEY) as client:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            quality="standard",
            n=1,
        )
    return response.data[0].url

print(
    # chatgpt("What is the capital of France?")
    # dalle("make a profile picture of a real person from france. like a social media profile pic. it should like like it was taken by a camera. like a normal person looking at a photo either doing some activity, with some friends, at a bar, outside, etc")
)