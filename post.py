import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os

def get_user_info(email):
    file_name = "users.json"  # Ensure your file name matches
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data.get(email, {})  # This should return a dictionary
    return {}

class Post:

    def __init__(self, root, user_email):
        self.user_email = user_email.get("mail")  # Store the logged email
        self.root = root
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")  # Dark background

        self.post_text = tk.StringVar()  # To store the entered text

        # Profile frame setup
        profile_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        profile_frame.pack(fill=tk.X, pady=(10, 0))

        # Profile image canvas with a circular profile
        self.profile_image_canvas = tk.Canvas(profile_frame, width=50, height=50, bg="#34495E", highlightthickness=0)
        self.profile_image_canvas.grid(row=0, column=0, padx=10)

        # Load default image until login is confirmed
        self.load_profile_image(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\book.jpg")

        # Profile name label
        self.name_label = tk.Label(profile_frame, text="", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
        self.name_label.grid(row=0, column=1, sticky='w')

        # Post frame setup
        post_frame = tk.Frame(self.root, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Text entry box for writing a post
        self.text_entry = tk.Entry(post_frame, textvariable=self.post_text, font=("Arial", 12), fg="#7F8C8D")
        self.text_entry.insert(0, "Write post here...")  # Default hint text
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.config(relief=tk.FLAT, bg="#ECF0F1", highlightbackground="#BDC3C7", highlightthickness=1)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(post_frame, bg="#ECF0F1")
        self.image_label.pack(pady=10)

        # Remove Image button
        self.remove_image_button = tk.Button(self.root, text="Remove Image", command=self.remove_image,
                                             bg="#E74C3E", fg="white", font=("Arial", 10), relief=tk.FLAT,
                                             cursor="hand2", borderwidth=0)
        self.remove_image_button.pack(pady=5)
        self.remove_image_button.pack_forget()  # Hide initially

        # Icon frame for the upload button
        icon_frame = tk.Frame(self.root, bg="#2C3E50")
        icon_frame.pack(pady=5)

        # Upload icon for adding images
        self.upload_icon = Image.open(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\camera.jpg")
        self.upload_icon = self.upload_icon.resize((50, 50))  # Resize icon
        self.upload_icon_photo = ImageTk.PhotoImage(self.upload_icon)

        upload_button = tk.Button(icon_frame, image=self.upload_icon_photo, command=self.upload_image, bg="#34495E",
                                  fg="white", relief=tk.FLAT, cursor="hand2", borderwidth=0)
        upload_button.pack(side=tk.LEFT, padx=5)

        # Post button to submit the post
        post_button = tk.Button(self.root, text="Post", command=self.post_content, bg="#1ABC9C", fg="white",
                                font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        post_button.pack(pady=10, ipadx=10, ipady=5)

        # Sort buttons
        sort_frame = tk.Frame(self.root, bg="#2C3E50")
        sort_frame.pack(pady=5)

        asc_button = tk.Button(sort_frame, text="Sort Ascending", command=self.view_posts_ascending, bg="#1ABC9C", fg="white")
        asc_button.pack(side=tk.LEFT, padx=5)

        desc_button = tk.Button(sort_frame, text="Sort Descending", command=self.view_posts_descending, bg="#E74C3E", fg="white")
        desc_button.pack(side=tk.LEFT, padx=5)

        # After login, set profile details
        self.set_user_profile(user_email)

    def load_profile_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((50, 50), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.profile_image_canvas.create_image(25, 25, image=img)  # Center image on canvas
            self.profile_image_canvas.image = img  # Keep reference to avoid garbage collection
        except Exception as e:
            print(f"Error loading image: {e}")

    def set_user_profile(self, user_email):
        user_details = self.get_user_details(user_email)
        self.name_label.config(text=user_details.get("name", "Unknown User"))
        profile_image_path = user_details.get("profile_image", None)
        if profile_image_path:
            self.load_profile_image(profile_image_path)
        else:
            self.load_profile_image(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\book.jpg")

    def get_user_details(self, user_email):
        file_name = "users.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
            user_details = data.get(user_email["mail"], {})
            return {
                "name": user_details.get("name", "Unknown User"),
                "profile_image": user_details.get("profile_image", None)
            }
        return {"name": "Unknown User", "profile_image": None}

    def clear_placeholder(self, event):
        if self.text_entry.get() == "Write post here...":
            self.text_entry.delete(0, tk.END)
            self.text_entry.config(fg="black")

    def add_placeholder(self, event):
        if self.text_entry.get() == "":
            self.text_entry.insert(0, "Write post here...")
            self.text_entry.config(fg="#7F8C8D")

    def upload_image(self):
        image_path = filedialog.askopenfilename(title="Select an image",
                                                filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            self.display_uploaded_image(image_path)
            self.uploaded_image_path = image_path  # Store image for later use in the post
            self.remove_image_button.pack()  # Show "Remove Image" button when already selected

    def display_uploaded_image(self, image_path):
        uploaded_img = Image.open(image_path)
        uploaded_img = uploaded_img.resize((100, 100))
        self.uploaded_img = ImageTk.PhotoImage(uploaded_img)
        self.image_label.config(image=self.uploaded_img)

    def load_posts_from_json(self):
        if os.path.exists("posts.json"):
            with open("posts.json", 'r') as f:
                data = json.load(f)
                for user_posts in data.values():
                    for post in user_posts:
                        # Ensure each post has a comments key
                        if "comments" not in post["content"]:
                            post["content"]["comments"] = []  # Initialize comments if not present

    def remove_image(self):
        self.image_label.config(image="")  # Clear the image label
        self.uploaded_image_path = None  # Remove image
        self.remove_image_button.pack_forget()  # Hide "Remove Image" button

    def post_content(self):
        post_text = self.post_text.get().strip()  # Get the entered text
        image_path = getattr(self, 'uploaded_image_path', None)  # Check if an image has been uploaded

        user_email = self.user_email  # Access the email directly

        if post_text and post_text != "Write post here...":
            post_data = {
                "content": {
                    "text": post_text,
                    "image": image_path,
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "likes": 0,
                    "comments": []
                }
            }
            self.save_post_to_json(post_data, user_email)  # Save the post to JSON
            self.view_posts()  # Refresh the post view
        else:
            print("No text entered for the post.")

    def save_post_to_json(self, post_data, user_email):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        if user_email not in data:
            data[user_email] = []

        post_id = len(data[user_email]) + 50
        post_data["id"] = post_id

        data[user_email].append(post_data)

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Post saved to {file_name}")

    def create_post(self, post_content, image_path=None):
        # Increment a post ID, could also be more sophisticated
        post_id = self.generate_post_id()
        post_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        new_post = {
            "id": post_id,
            "content": {
                "text": post_content,
                "date": post_date,
                "image": image_path,
                "likes": 0,  # Initialize likes
                "comments": []  # Initialize comments list
            }
        }

        # Load existing posts
        if os.path.exists("posts.json"):
            with open("posts.json", 'r') as f:
                data = json.load(f)
        else:
            data = {}

        # Save the new post under the user's email
        user_email = self.user_email
        if user_email not in data:
            data[user_email] = []
        data[user_email].append(new_post)

        self.save_posts_to_json(data)

    def view_posts(self):
        self.clear_post_view()
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            user_posts = data.get(self.user_email, [])
            for post in user_posts:
                self.display_post(post["content"], post["id"])



    def clear_post_view(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.root.winfo_children()[0]:  # Keep profile frame
                widget.destroy()

    def display_post(self, post_content, post_id):
        post_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        post_frame.pack(pady=5, fill=tk.X)

        post_text = post_content["text"]
        post_date = post_content["date"]
        post_image_path = post_content["image"]

        post_label = tk.Label(post_frame, text=post_text, bg="#34495E", fg="white", wraplength=400, justify=tk.LEFT)
        post_label.pack()

        date_label = tk.Label(post_frame, text=post_date, bg="#34495E", fg="white", font=("Arial", 8))
        date_label.pack()

        if post_image_path:
            img = Image.open(post_image_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            image_label = tk.Label(post_frame, image=img, bg="#34495E")
            image_label.image = img  # Keep a reference
            image_label.pack()

        # Make sure to access likes correctly
        likes_count = post_content.get("likes", 0)  # Use .get() to avoid KeyError
        likes_label = tk.Label(post_frame, text=f"Likes: {likes_count}", bg="#34495E", fg="white")
        likes_label.pack(side=tk.LEFT, padx=5)

        # Comment button
        comment_button = tk.Button(post_frame, text="Comment", command=lambda: self.comment_on_post(post_id),
                                   bg="#1ABC9C", fg="white")
        comment_button.pack(side=tk.LEFT, padx=5)

        # Display comments
        comments = post_content.get("comments", [])
        for comment in comments:
            comment_label = tk.Label(post_frame, text=comment, bg="#34495E", fg="white", wraplength=400,
                                     justify=tk.LEFT)
            comment_label.pack()

    def like_post(self, post_id):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            for user_posts in data.values():
                for post in user_posts:
                    if post.get("id") == post_id:
                        post["content"]["likes"] += 1  # Increment the likes count
                        self.save_posts_to_json(data)  # Save changes
                        self.view_posts()  # Refresh post view
                        return
        print("Post not found.")

    def comment_on_post(self, post_id):
        comment = simpledialog.askstring("Comment", "Enter your comment:")
        if comment:
            # Load posts first to find the correct post
            with open("posts.json", 'r') as f:
                data = json.load(f)

            user_email = self.user_email
            for post in data.get(user_email, []):
                if post["id"] == post_id:
                    # Ensure the comments list exists
                    if "comments" not in post["content"]:
                        post["content"]["comments"] = []  # Initialize if missing

                    post["content"]["comments"].append(comment)  # Add the comment

                    # Save the updated post back to JSON
                    self.save_posts_to_json(data)
                    break

    def save_posts_to_json(self, data):
        with open("posts.json", 'w') as f:
            json.dump(data, f, indent=4)

    def view_posts_ascending(self):
        self.clear_post_view()
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            user_posts = data.get(self.user_email, [])
            sorted_posts = sorted(user_posts, key=lambda x: datetime.strptime(x["content"]["date"], "%d-%m-%Y %H:%M:%S"))
            for post in sorted_posts:
                self.display_post(post["content"], post["id"])

    def view_posts_descending(self):
        self.clear_post_view()
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            user_posts = data.get(self.user_email, [])
            sorted_posts = sorted(user_posts, key=lambda x: datetime.strptime(x["content"]["date"], "%d-%m-%Y %H:%M:%S"), reverse=True)
            for post in sorted_posts:
                self.display_post(post["content"], post["id"])

# Sample main application setup
if __name__ == "__main__":
    root = tk.Tk()
    user_email = {"mail": "test@example.com"}  # Replace with actual user email during login
    app = Post(root, user_email)
    root.mainloop()
