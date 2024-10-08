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
        'mood': moods,
        'comment_content': [None] * n  # Placeholder for comments
    }

    comments = pd.DataFrame(comments)
    comments['id'] = range(comments.shape[0])

    post_prompt = """
    You are a user. Your name is {user[name]}. Here are your characteristics:

    Temperature: {user[temperature]}
    Nationality: {user[nationality]}
    Political Ideology Leaning: {user[political_ideology_leaning]}
    Interests: {user[interests]}
    Your Personal Mood: {user[mood]}
    Personality Type: {user[personality_type]}

    You scrolled and found a post: {post[post-content]}

    Mood intensity ranges from -1.0 (less intense) to 1.0 (more intense). Your current mood intensity is: [{mood}]. Respond accordingly.

    The person who made this post is: {user}. Consider how they align with your personality when you make your response.

    Return your answer as just the text of your comment.
    """

    # Create the prompt for each comment
    comments['prompt'] = comments.apply(lambda row: post_prompt.format(user=row['user'], post=row['post'], mood=row['mood']), axis=1)

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
    
    # build sqlite3 connection to path `./db.sqlite` with pythons sqlite module
    conn = sqlite3.connect('./db.sqlite')
    comments.to_sql('comments', conn, if_exists='replace', index=False)
