# python standard library
import os, random, json, sqlite3, datetime

# third party
import numpy as np
import pandas as pd

# local
import ai

conn = sqlite3.connect('./db.sqlite')

# Load user profiles
users = pd.read_sql('select * from profiles', conn)

def generate_posts(n=1):
    # Ensure n is an integer
    n = int(n)

    # Initialize LLM function references
    llm = ai.chatgpt
    image_model = ai.dalle  

    # Declare post attributes in a single dictionary
    posts = {
        'post_type': np.random.choice(
            [
                "humor", "personal reflection", "recommendations", 
                "random thoughts", "reflection on current events", 
                "news event", "political opinion", "motivation/inspiration", 
                "funny story", "travel experience", "accomplishment",
                "sports",
            ], size=n
        ),
        'suggest_post_length': np.random.choice(
            [1, 2, 3], size=n, p=[0.35, 0.55, 0.1]  # Setting weights for selection
        ),
    }

    posts = pd.DataFrame(posts)

    posts['id'] = range(posts.shape[0])

    # Add a random date ranging from today to 6 months ago
    posts['date'] = pd.to_datetime(np.random.choice(pd.date_range(datetime.datetime.now() - datetime.timedelta(days=180), datetime.datetime.now()), size=n))

    # Randomly sample a user from the users DataFrame
    posts['user'] = np.random.choice(users.to_dict(orient='records'), size=n)

    post_prompt = """
    You are a user. Your name is {name}. Here are your characteristics:

    Nationality: {nationality}
    Interests: {interests}
    Mood: {mood}
    Personality Type: {personality_type}

    Write a tweet-like post with the following characteristics:

    Post Type: {post_type}
    Suggested Post Length (in sentences): {suggest_post_length}

    Return your answer as just the text of your post. 
    """

    # Create the prompt for each post
    posts['prompt'] = posts.apply(
        lambda row: post_prompt.format(
            post_type = row['post_type'], 
            suggest_post_length = row['suggest_post_length'], 
            **row['user']
        ), 
        axis = 1,
    )
    # print(posts['prompt'].loc[0]); exit()
    
    posts['post-content'] = posts.apply(lambda row: llm(row['prompt']), axis=1)
    
    posts['user'] = posts['user'].apply(lambda user: user['id'])

    # Return the posts DataFrame as a list of dictionaries
    return posts

# Example usage
if __name__ == "__main__":
    number_of_posts = os.environ.get('NUM_POSTS', 100)
    posts = generate_posts(number_of_posts)
     
    # build sqlite3 connection to path `./db.sqlite` with pythons sqlite module
    conn = sqlite3.connect('./db.sqlite')
    posts.to_sql('posts', conn, if_exists='replace', index=False)
