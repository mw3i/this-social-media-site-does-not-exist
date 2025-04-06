# python standard library
import os, random, json, sqlite3, datetime

# third party
import numpy as np
import pandas as pd
import dotenv
dotenv.load_dotenv('config')

# local
import ai

conn = sqlite3.connect('./db.sqlite')

users = pd.read_sql('select * from profiles', conn)
posts = pd.read_sql('select * from posts', conn)

def generate_comments(n=1):
    # Ensure n is an integer
    n = int(n)

    # Initialize LLM function references
    llm = ai.chatgpt
    image_model = ai.dalle  

    # Randomly sample mood values
    mood_mean = float(os.environ.get('COMMENT_MOOD_INTENSITY_MEAN', 0))
    moods = np.random.normal(loc=mood_mean, scale=0.5, size=n)  # Adjust scale as needed
    moods = np.clip(moods, -1, 1)  # Ensure moods are between -1 and 1

    # Randomly sample users and posts
    sampled_users = np.random.choice(users.to_dict(orient='records'), size=n)
    sampled_posts = np.random.choice(posts.to_dict(orient='records'), size=n)

    # Declare comment attributes in a single dictionary
    comments = {
        'user': sampled_users,
        'post': sampled_posts,
        'comment_content': [None] * n  # Placeholder for comments
    }

    comments = pd.DataFrame(comments)
    comments['id'] = range(comments.shape[0])

    # comments['poster'] = comments.apply(lambda row: row['post'], axis = 1)
    comments['poster'] = comments.apply(lambda row: users[users['id'] == row['post']['user']].iloc[0].to_dict(), axis = 1)

    post_prompt = """
    You are a user on a social media site. Your name is {name}. Here are your characteristics:

    Nationality: {nationality}
    Interests: {interests}
    Your Personal Mood: {mood}
    Personality Type: {personality_type}

    You scrolled and found a post: 
    ```
    {post_content}
    ```

    The person who made this post is: 

        name: {poster_name}
        interests: {poster_interests}
        personality_type: {poster_personality_type}

    Consider how they align with your personality when you make your response.

    Return your answer as just the text of your comment. 1-2 sentences, 3 if needed
    """
    # Create the prompt for each comment

    comments['prompt'] = comments.apply(
        lambda row: post_prompt.format(
            post_content = row['post']['post-content'],
            poster_name = row['poster']['name'],
            poster_interests = row['poster']['interests'],
            poster_personality_type = row['poster']['personality_type'],
            **row['user'],
        ), 
        axis=1
    )

    comments['comment_content'] = comments.apply(lambda row: llm(row['prompt']), axis=1)
    comments['user'] = comments['user'].apply(lambda user: user['id'])
    comments['post'] = comments['post'].apply(lambda post: post['id'])

    # Add a random date ranging from today to 6 months ago
    comments['date'] = pd.to_datetime(np.random.choice(pd.date_range(datetime.datetime.now() - datetime.timedelta(days=180), datetime.datetime.now()), size=n))

    # Return the comments DataFrame as a list of dictionaries
    return comments

# Example usage
if __name__ == "__main__":
    number_of_comments = os.environ.get('NUM_COMMENTS', 100)
    comments = generate_comments(number_of_comments)
    
    comments['poster'] = comments['poster'].apply(lambda x: json.dumps(x))
    
    # build sqlite3 connection to path `./db.sqlite` with pythons sqlite module
    conn = sqlite3.connect('./db.sqlite')
    comments.to_sql('comments', conn, if_exists='replace', index=False)
