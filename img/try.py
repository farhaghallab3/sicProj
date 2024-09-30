import json
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


class Post:
    def __init__(self, root , likes):
        self.root = root
        self.root.geometry("500x600")
        self.root.configure(bg="#2C3E50")

        self.stack = Stack()  # Initialize the page stack for navigation
        self.post_text = tk.StringVar()

        # Main frame (for Create Post page)
        self.main_frame = tk.Frame(self.root, bg="#2C3E50")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Profile frame
        profile_frame = tk.Frame(self.main_frame, bg="#34495E", padx=10, pady=10)
        profile_frame.pack(fill=tk.X, pady=(10, 0))

        self.profile_image_canvas = tk.Canvas(profile_frame, width=50, height=50, bg="#34495E", highlightthickness=0)
        self.profile_image_canvas.grid(row=0, column=0, padx=10)

        self.load_profile_image(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\book.jpg")

        name_label = tk.Label(profile_frame, text="Farha Ghallab", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
        name_label.grid(row=0, column=1, sticky='w')

        # Post frame
        post_frame = tk.Frame(self.main_frame, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.text_entry = tk.Entry(post_frame, textvariable=self.post_text, font=("Arial", 12), fg="#7F8C8D")
        self.text_entry.insert(0, "Write post here...")
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.config(relief=tk.FLAT, bg="#ECF0F1", highlightbackground="#BDC3C7", highlightthickness=1)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(post_frame, bg="#ECF0F1")
        self.image_label.pack(pady=10)

        # Icon frame for upload
        icon_frame = tk.Frame(self.main_frame, bg="#2C3E50")
        icon_frame.pack(pady=5)

        self.upload_icon = Image.open(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\camera.jpg")
        self.upload_icon = self.upload_icon.resize((50, 50))
        self.upload_icon_photo = ImageTk.PhotoImage(self.upload_icon)

        upload_button = tk.Button(icon_frame, image=self.upload_icon_photo, command=self.upload_image, bg="#34495E",
                                  fg="white", relief=tk.FLAT, cursor="hand2", borderwidth=0)
        upload_button.pack(side=tk.LEFT, padx=5)

        post_button = tk.Button(self.main_frame, text="Post", command=self.post_content, bg="#1ABC9C", fg="white",
                                font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        post_button.pack(pady=10, ipadx=10, ipady=5)

        view_posts_button = tk.Button(self.main_frame, text="View Posts", command=self.switch_to_posts_page,
                                      bg="#2980B9",
                                      fg="white", font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        view_posts_button.pack(pady=10)

        # Frame to hold the view posts page
        self.posts_frame = tk.Frame(self.root, bg="#2C3E50")

        # Title label for view posts
        self.title_label = tk.Label(self.posts_frame, text="View Posts", font=("Arial", 16, "bold"), bg="#2C3E50", fg="white")
        self.title_label.pack(pady=(10, 5))

        # Back button (for going back to the previous page)
        self.back_button = tk.Button(self.posts_frame, text="Back", command=self.go_back, bg="#E74C3C", fg="white",
                                     font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        self.back_button.pack(pady=(0, 0))  # Positioned at the top left

        # Add canvas and scrollbar for the posts section
        self.canvas = tk.Canvas(self.posts_frame, bg="#ECF0F1")
        self.scrollbar = tk.Scrollbar(self.posts_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.content_frame = tk.Frame(self.canvas, bg="#ECF0F1")
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Bind scroll region update
        self.content_frame.bind("<Configure>",
                                lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.posts = []
        self.comments = []
        self.sort_option = "date"
        self.sort_option = tk.StringVar(value="likes")  # Default sorting option
        self.sort_order = tk.StringVar(value='ascending')  # Default order
        self.likes = likes
        self.post_frames = []

    def load_profile_image(self, image_path: str):
        img = Image.open(image_path)
        img = img.resize((50, 50))
        self.profile_img = ImageTk.PhotoImage(img)
        self.profile_image_canvas.create_oval(5, 5, 45, 45, outline="#1ABC9C", width=2)
        self.profile_image_canvas.create_image(25, 25, image=self.profile_img)

    def clear_placeholder(self, event):
        if self.text_entry.get() == "Write post here...":
            self.text_entry.delete(0, tk.END)
            self.text_entry.config(fg="black")

    def add_placeholder(self, event):
        if not self.text_entry.get().strip():
            self.text_entry.insert(0, "Write post here...")
            self.text_entry.config(fg="#7F8C8D")

    def upload_image(self):
        image_path = filedialog.askopenfilename(title="Select an image",
                                                filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            self.display_uploaded_image(image_path)
            self.uploaded_image_path = image_path

    def display_uploaded_image(self, image_path):
        uploaded_img = Image.open(image_path)
        uploaded_img = uploaded_img.resize((100, 100))
        self.uploaded_img = ImageTk.PhotoImage(uploaded_img)
        self.image_label.config(image=self.uploaded_img)

    def post_content(self):
        post_text = self.post_text.get().strip()
        image_path = getattr(self, 'uploaded_image_path', None)
        if post_text != "" and post_text != "Write post here...":

            post_data = {
                "content": {
                    "text": post_text,
                    "image": image_path,
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M")
                },
                "likes": 0,  # Initialize likes
                "liked_by": [],  # Initialize liked_by
                "comments": [],  # Initialize comments
                "id": self.get_next_post_id()  # Get the next post ID
            }

            post_data["id"] = self.get_next_post_id()
            self.posts.append(post_data)  # Add post to the list of posts
            self.save_post_to_json(post_data)
            self.display_post(self.content_frame, post_data)  # Automatically display post after creating it
            print("Post created successfully.")
        else:
            print("No text entered for the post.")




    def get_next_post_id(self):
        file_name = "posts.json"

        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                try:
                    data = json.load(f)  # Load the data


                    max_id = 0

                    for user_posts in data.values():
                        if isinstance(user_posts, list):
                            for post in user_posts:
                                if isinstance(post, dict) and 'id' in post:
                                    post_id = post['id']
                                    if post_id > max_id:
                                        max_id = post_id
                                else:
                                    print("Expected a dictionary for post, but got:",
                                          post)
                        else:
                            print("Expected a list of posts, but got:", user_posts)  # Debug: print unexpected type
                except json.JSONDecodeError:
                    print("JSONDecodeError: File might be corrupted. Initializing ID to 0.")
                    return 0
        else:
            return 0

        return max_id + 1

    def save_post_to_json(self, post_data):
        file_name = "posts.json"

        # Load existing data
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print("JSONDecodeError: File might be corrupted. Starting fresh.")
                    data = {}
        else:
            data = {}

        user_email = ''

        # If the user key does not exist, initialize it
        if user_email not in data:
            data[user_email] = []

        # Append the new post data
        data[user_email].append(post_data)

        # Save back to the JSON file
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def display_post(self, frame, post_data):
        post_frame = tk.Frame(frame)
        post_frame.pack()
        comment_frame = tk.Frame(post_frame)
        comment_frame.pack()


        if self.post_frames:
            self.post_frames[-1]['comments_frame'] = comment_frame
        else:
            # Handle the case where post_frames is empty
            print("Error: post_frames is empty.")

        self.sort_comments_by_date(post_data["comments"])

        # Create a frame for displaying the post
        post_frame = tk.Frame(frame, bg="#ECF0F1", padx=10, pady=10, bd=2, relief=tk.GROOVE)
        post_frame.pack(fill=tk.X, pady=5)

        # Display post content
        content_label = tk.Label(post_frame, text=post_data["content"]["text"], bg="#ECF0F1", wraplength=300)
        content_label.pack(anchor='w')

        # Display post image if available
        if post_data["content"]["image"]:
            post_image = Image.open(post_data["content"]["image"])
            post_image = post_image.resize((100, 100))
            post_image_photo = ImageTk.PhotoImage(post_image)
            image_label = tk.Label(post_frame, image=post_image_photo, bg="#ECF0F1")
            image_label.image = post_image_photo  # Keep a reference to avoid garbage collection
            image_label.pack(anchor='w')

        # Display post date
        date_label = tk.Label(post_frame, text=post_data["content"]["date"], bg="#ECF0F1", fg="#7F8C8D")
        date_label.pack(anchor='w')

        # Like button
        like_button = tk.Button(post_frame, text=f"Like ({post_data['likes']})",
                                command=lambda: self.like_post(post_data),
                                bg="#3498DB", fg="white", font=("Arial", 10), relief=tk.RAISED, cursor="hand2")
        like_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=5)

        # Comment section
        comment_frame = tk.Frame(post_frame, bg="#ECF0F1")
        comment_frame.pack(fill=tk.X)

        self.comment_entry = tk.Entry(comment_frame, width=30)
        self.comment_entry.pack(side=tk.LEFT, padx=(0, 5))

        comment_button = tk.Button(comment_frame, text="Comment",
                                   command=lambda: self.add_comment(post_data["id"], self.comment_entry.get()),
                                   bg="#E67E22", fg="white", font=("Arial", 10), relief=tk.RAISED, cursor="hand2")
        comment_button.pack(side=tk.LEFT)


        # Display existing comment
        if 'comments' in post_data:
            for comment in post_data['comments']:
                self.display_comment(post_data['id'], comment)

        self.post_frames.append({'comments_frame': comment_frame})
        self.post_frames.append({"id": post_data["id"], "comments_frame": comment_frame})


    def display_comment(self, post_id, comment_data):
        # Find the post's comment section in the UI
        for post_frame in self.post_frames:
            if post_frame['id'] == post_id:
                comments_frame = post_frame['comments_frame']  # Assuming you stored references to frames
                # Create a label for the new comment
                comment_label = tk.Label(comments_frame, text=comment_data["text"], bg="#ECF0F1", anchor='w')
                comment_label.pack(anchor='w')  # Align left
                break



    def show_posts(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Retrieve the current sort option and order
        option = self.sort_option.get()
        order = self.sort_order.get()

        # Sort posts based on the selected option and order
        if option == "date":
            self.posts.sort(key=lambda post: datetime.strptime(post["content"]["date"], "%d-%m-%Y %H:%M"),
                            reverse=(order == 'descending'))
        elif option == "likes":
            self.posts.sort(key=lambda post: post["likes"], reverse=(order == 'descending'))

        # Create sorting buttons
        sort_by_date_asc_button = tk.Button(self.content_frame, text="Sort by Date Ascending",
                                            command=lambda: self.change_sort_option("date", "ascending"))
        sort_by_date_desc_button = tk.Button(self.content_frame, text="Sort by Date Descending",
                                             command=lambda: self.change_sort_option("date", "descending"))

        sort_by_date_asc_button.pack(pady=(5, 10))
        sort_by_date_desc_button.pack(pady=(5, 10))

        for post in self.posts:
            self.display_post(self.content_frame, post)



    def update_post_in_json(self, post_data):
        """Update the post data in the JSON file."""
        try:
            with open('posts.json', 'r') as file:
                posts = json.load(file)  # This should load a list of posts

            # Find the post to update
            for post in posts:
                if post["id"] == post_data["id"]:
                    post.update(post_data)  # Update the post with new data
                    break

            # Save the updated posts back to the JSON file
            with open('posts.json', 'w') as file:
                json.dump(posts, file, indent=4)
        except json.JSONDecodeError:
            print("Error decoding JSON from file. Please check the file format.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def like_post(self, post_id):
        file_name = "posts.json"

        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                try:
                    data = json.load(f)
                    # Make sure data is as expected
                    for user_email, user_posts in data.items():
                        if isinstance(user_posts, list):  # Ensure user_posts is a list
                            for post in user_posts:
                                if isinstance(post, dict) and post['id'] == post_id:
                                    post['likes'] += 1
                                    post['liked_by'].append("user@example.com")  # Use the actual email here
                                    break
                except json.JSONDecodeError:
                    print("JSONDecodeError: File might be corrupted.")
                    return
                except Exception as e:
                    print(f"An error occurred: {e}")

            # Save back to JSON
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
            print("Post liked successfully!")

    def add_comment(self, post_id, comment_text):
        file_name = "posts.json"

        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                try:
                    data = json.load(f)
                    # Make sure data is as expected
                    for user_email, user_posts in data.items():
                        if isinstance(user_posts, list):
                            for post in user_posts:
                                if isinstance(post, dict) and post['id'] == post_id:
                                    comment = {
                                        "user": "user@example.com",  # Replace with actual user email
                                        "content": comment_text,
                                        "date": "29-09-2024 15:38",  # Replace with current date/time
                                        "likes": 0,
                                        "liked_by": [],
                                        "replies": []
                                    }
                                    # Append the comment to the post's comments list
                                    if 'comments' not in post:
                                        post['comments'] = []  # Initialize if comments list doesn't exist
                                    post['comments'].append(comment)

                                    # Call display_comment to update UI
                                    self.display_comment(post_id, comment)
                                    break
                except json.JSONDecodeError:
                    print("JSONDecodeError: File might be corrupted.")
                    return
                except Exception as e:
                    print(f"An error occurred: {e}")

            # Save back to JSON
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
            print("Comment added successfully!")

    def switch_to_posts_page(self):
        self.stack.push(self.main_frame)
        self.main_frame.pack_forget()
        self.posts_frame.pack(fill=tk.BOTH, expand=True)
        self.show_posts()
        self.back_button.pack(pady=(10, 0))

    def sort_comments_by_date(self, comments, ascending=True):
        comments.sort(key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y %H:%M"), reverse=not ascending)

    def go_back(self):
        self.posts_frame.pack_forget()  # Hide the posts page
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # Show the create post page

    def load_posts(self):
        for post in self.posts:
            self.display_post(self.content_frame, post)

    def run(self):
        self.root.mainloop()






if __name__ == "__main__":
    root = tk.Tk()
    app = Post(root,likes='')
    app.run()
