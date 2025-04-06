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
        'nationality': [
            random.choice([
                "United States"
            ]) for _ in range(n)
        ],
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

    # Reformat interests
    users['interests'] = users['interests'].apply(lambda x: ', '.join(x))

    # Add an 'id' column with a range of values starting from 1
    users['id'] = range(users.shape[0])

    # Prompt for generating a random name
    name_prompt = '''
    Generate a random English first and last name for a social media user.

    Their information:

    Nationality: {nationality}
    Personality Type: {personality_type}
    Interests: {interests}

    Return answer as a simple string formatted: first name, last name
    '''

    def getname(row):
        # Format interests into a clean string
        prompt = name_prompt.format(**row.to_dict())
        res = llm(prompt)
        print('built', row['id'], 'w/', prompt, '\nres:', res)
        return res

    users['name'] = users.apply(lambda row: getname(row), axis = 1)

    # users['name'] = users.apply(lambda row: llm(name_prompt.format(user = row), temp = 2), axis = 1)
    # users['name'] = users.apply(lambda row: name_prompt.format(user = row), axis = 1)

    # Prompt for generating a profile image
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
