import json

def friend_posts_read():
    # Specify encoding as 'utf-8' while opening the files
    try:
        with open("friends.json", "r", encoding="utf-8") as file:
            friends = json.load(file)
        with open("posts.json", "r", encoding="utf-8") as file:
            posts = json.load(file)
    except UnicodeDecodeError as e:
        print("Error decoding file:", e)
    except FileNotFoundError as e:
        print("File not found:", e)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    return friends, posts

def view_post(post):
    print(post)
