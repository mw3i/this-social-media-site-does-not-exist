# python standard library
import os, random, json, sqlite3

# third party
import numpy as np
import pandas as pd

# local
import ai


conn = sqlite3.connect('./db.sqlite')

def generate_profiles(n):
    # Ensure n is an integer
    n = int(n)

    # Initialize LLM function references
    llm = ai.chatgpt
    image_model = ai.dalle  

    # Declare user attributes in a single dictionary
    users = {
        'temperature': np.random.normal(0, 1, n),  # n samples from a normal distribution
        'nationality': [
            random.choice([
                "United States", "China", "Japan", "Germany", "India", 
                "United Kingdom", "France", "Italy", "Brazil", "Canada"
            ]) for _ in range(n)
        ],
        'political_ideology_leaning': np.random.uniform(0, 1, n),  # Random values between 0 and 1
        'interests': [
            random.sample([
                "sports", "politics", "gardening", "reading", "traveling",
                "cooking", "music", "art", "technology", "fitness",
                "photography", "gaming", "fashion", "writing", "history",
                "movies", "hiking", "volunteering", "science", "education",
                "pets"
            ], k=random.randint(1, 5)) for _ in range(n)  # Sample 1 to 5 interests
        ],
        'mood': [
            random.choice([
                "happy", "sad", "angry", "excited", "bored", 
                "anxious", "calm", "confident", "disappointed", "curious",
                "frustrated", "relaxed", "hopeful", "overwhelmed", "content",
                "nostalgic", "fearful", "surprised", "grateful", "lonely"
            ]) for _ in range(n)
        ],
        'personality_type': [
            random.choice([
                "jokester", "bully", "motivational type", "snob",
                "friendly person", "intellectual", "adventurous", "introvert",
                "extrovert", "caregiver", "thinker", "doer", 
                "innovator", "traditionalist", "dreamer", "realist"
            ]) for _ in range(n)
        ],
    }
    users = pd.DataFrame(users)

    # Add an 'id' column with a range of values starting from 1
    users['id'] = range(users.shape[0])

    # Prompt for generating a random name
    name_prompt = '''Generate a random first and last name for a social media user based on their nationality: {user[nationality]}. return answer as just the string<<first name, last name>> (but leave out the << and >> obviously)'''
    users['name'] = users.apply(lambda row: llm(name_prompt.format(user = row)), axis = 1)

    # Prompt for generating a profile image
    image_prompt = "Generate a profile image for a social media user."
    users['profile_pic_path'] = ''

    # json cols
    users['interests'] = users['interests'].apply(json.dumps)

    # Return the users df
    return users

# Example usage
if __name__ == "__main__":
    number_of_profiles = os.environ.get('NUM_PROFILES', 100)
    profiles = generate_profiles(number_of_profiles)

    # build sqlite3 connection to path `./db.sqlite` with pythons sqlite module
    profiles.to_sql('profiles', conn, if_exists='replace', index=False)
