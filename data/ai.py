import os, time, functools

import openai
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv('../env')

# Fetch OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the API key is available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Make sure it's in the .env file.")

def retry_on_exception(max_retries=3, wait_seconds=60, exceptions=(openai.RateLimitError,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_retries:
                        print(f"[ERROR] Max retries reached for {func.__name__}. Raising exception.")
                        return None
                    print(f"[RETRY] {func.__name__} failed with {e.__class__.__name__}: {e}")
                    print(f"Waiting {wait_seconds} seconds before retrying... ({attempts}/{max_retries})")
                    time.sleep(wait_seconds)
        return wrapper
    return decorator

# Function to send a prompt to the OpenAI ChatGPT model and return the text response
@retry_on_exception()
def chatgpt(prompt, temp = None, model="gpt-4o"):
    # Use the OpenAI client as a context manager
    with openai.OpenAI(api_key=OPENAI_API_KEY) as client:
        print('\n\n',prompt,'\n\n')
        chat_completion = client.chat.completions.create(
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model = model,
            **{'temperature': temp} if temp else {},
        )
        return chat_completion.choices[0].message.content.strip()

# Function to send a prompt to the OpenAI Dalle model and return image response
@retry_on_exception()
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

# print(
    # chatgpt("What is the capital of France?")
    # dalle("make a profile picture of a real person from france. like a social media profile pic. it should like like it was taken by a camera. like a normal person looking at a photo either doing some activity, with some friends, at a bar, outside, etc")
# )