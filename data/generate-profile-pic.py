# Import necessary modules
import os, random, sqlite3

import requests

from ai import dalle

# Establish the database connection
conn = sqlite3.connect('./db.sqlite')
conn.row_factory = sqlite3.Row

imgdir = '../frontend/-/images'

# Save the generated image to a file
def save_image(image_url, profile_id):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(f"{imgdir}/{profile_id}.png", "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download image for profile {profile_id}")

# Main execution
if __name__ == "__main__":
    profiles = (
        conn
        .cursor()
        .execute(
            "SELECT * FROM profiles"
        )
        .fetchall()
    )
    profiles = [dict(profile) for profile in profiles]

    img_options = [
        'the person is hanging out with friends',
        'the person is doing one of the activities they are interested in',
        'it\'s just a picture of the persons face',
    ]

    for profile in profiles:
        print(profile['name'], profile['id'])
        if os.path.exists(f"{imgdir}/{profile['id']}.png"):
            print('img already exists')
        else:

            prompt = f"""A realistic, real social media profile picture for this person: 

            {profile}

            where: {random.choice(img_options)}
            """

            try:
                # Generate image using dalle function from ai module
                image_url = dalle(prompt)
                print(f"Generated image")
                
                # Save the generated image
                save_image(image_url, profile['id'])
                print(f"Saved image successfully")
            
            except Exception as e:
                print(f"Failed to generate or save image")


    # Close the database connection
    conn.close()
