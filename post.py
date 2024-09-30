import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import os



class Post:

    def __init__(self, root, user_email):
        self.user_email = user_email.get("mail")  # Store the logged email
        self.root = root
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")  # Dark background

        self.post_text = tk.StringVar()  # To store the entered text
        self.uploaded_image_path = None

        # Create the navigation bar at the top
        self.create_navigation_bar()

        self.page_history = []
        self.current_page_index = -1

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
        self.post_frame = tk.Frame(self.root, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
        self.post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Text entry box for writing a post
        self.text_entry = tk.Entry(self.post_frame, textvariable=self.post_text, font=("Arial", 12), fg="#7F8C8D")
        self.text_entry.insert(0, "Write post here...")  # Default hint text
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.config(relief=tk.FLAT, bg="#ECF0F1", highlightbackground="#BDC3C7", highlightthickness=1)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(self.post_frame, bg="#ECF0F1")
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

    def remove_image(self):
        self.image_label.config(image="")  # Clear the image label
        self.uploaded_image_path = None  # Remove image
        self.remove_image_button.pack_forget()  # Hide "Remove Image" button

    def post_content(self):
        post_text = self.post_text.get().strip()  # Get the entered text
        image_path = getattr(self, 'uploaded_image_path', None)  # Check if an image has been uploaded
        user_email = self.user_email  # Access the email directly

        if post_text and post_text != "Write post here...":
            user_details = self.get_user_details(user_email)
            post_data = {
                "content": {
                    "text": post_text,
                    "image": image_path,
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "likes": 0,
                    "comments": []
                },
                "user": {
                    "name": user_details.get("name", "Unknown User"),
                    "profile_image": user_details.get("profile_image",
                                                      r"C:\Users\farha\OneDrive\Desktop\sicProj\img\book.jpg")
                }
            }
            self.save_post_to_json(post_data, user_email)  # Save the post to JSON
            self.view_posts()  # Switch to view posts after creating
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

        print(f"Post saved to {file_name}: {post_data}")

    def create_navigation_bar(self):
        nav_bar = tk.Frame(self.root, bg="#2C3E50", padx=10, pady=5)
        nav_bar.pack(fill=tk.X)

        back_button = tk.Button(nav_bar, text="Back", bg="#1ABC9C", fg="white", font=("Arial", 10),
                                relief=tk.FLAT, cursor="hand2", command=self.go_back)
        back_button.pack(side=tk.LEFT, padx=5)

        forward_button = tk.Button(nav_bar, text="Forward", bg="#1ABC9C", fg="white", font=("Arial", 10),
                                   relief=tk.FLAT, cursor="hand2", command=self.go_forward)
        forward_button.pack(side=tk.LEFT, padx=5)

        home_button = tk.Button(nav_bar, text="My Home", bg="#1ABC9C", fg="white", font=("Arial", 10),
                                relief=tk.FLAT, cursor="hand2", command=self.go_home)
        home_button.pack(side=tk.LEFT, padx=5)

        profile_button = tk.Button(nav_bar, text="My Profile", bg="#1ABC9C", fg="white", font=("Arial", 10),
                                   relief=tk.FLAT, cursor="hand2", command=self.go_profile)
        profile_button.pack(side=tk.LEFT, padx=5)

        request_friend_button = tk.Button(nav_bar, text="My Request Friend", bg="#1ABC9C", fg="white",
                                          font=("Arial", 10),
                                          relief=tk.FLAT, cursor="hand2", command=self.request_friend)
        request_friend_button.pack(side=tk.LEFT, padx=5)

        logout_button = tk.Button(nav_bar, text="Log Out", bg="#E74C3C", fg="white", font=("Arial", 10),
                                  relief=tk.FLAT, cursor="hand2", command=self.log_out)
        logout_button.pack(side=tk.RIGHT, padx=5)

    def navigate_to_page(self, page_function):
        """Helper function to navigate to a specific page."""
        print(f"Navigating to {page_function.__name__}")

        # Clear current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Recreate navigation bar and load the target page
        self.create_navigation_bar()
        page_function()  # Call the page function

    def go_back(self):
        if self.current_page_index > 0:
            print("Going Back")
            self.current_page_index -= 1
            self.navigate_to_page(self.page_history[self.current_page_index])
        else:
            print("Cannot go back further")

    def go_forward(self):
        if self.current_page_index < len(self.page_history) - 1:
            self.current_page_index += 1
            self.navigate_to_page(self.page_history[self.current_page_index])



    def go_home(self):
        self.add_to_history(self.go_home)
        self.navigate_to_page(self.view_posts())

    def go_profile(self):
        self.add_to_history(self.go_profile)
        self.navigate_to_page(self.view_posts())


    def request_friend(self):
        self.add_to_history(self.go_profile)
        self.navigate_to_page(self.view_posts())

    def log_out(self):
        self.add_to_history(self.log_out)
        self.navigate_to_page(self.view_posts())

    def add_to_history(self, page_function):
        """Add the current page function to history and update the index."""
        if self.current_page_index < len(self.page_history) - 1:
            # Clear forward history if the user navigated backward
            self.page_history = self.page_history[:self.current_page_index + 1]

        self.page_history.append(page_function)
        self.current_page_index = len(self.page_history) - 1  # Update index to new page

    def view_posts(self):

        self.add_to_history(self.view_posts)
        # Clear the current window and remove the post creation elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Recreate the navigation bar at the top
        self.create_navigation_bar()  # This will add the navigation bar

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self.root, bg="#ECF0F1")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure the scrollable frame
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a window in the canvas for the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack the canvas and scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Show user posts
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            # Collect all posts
            posts = []
            for user_posts in data.values():
                posts.extend(user_posts)

            # Filter out invalid post formats
            valid_posts = []
            for post in posts:
                if isinstance(post, dict) and "content" in post and "date" in post["content"]:
                    valid_posts.append(post)
                else:
                    print(f"Invalid post format: {post}")

            # Sort valid posts by date (latest first)
            valid_posts.sort(key=lambda x: x["content"]["date"], reverse=True)

            # Display each valid post
            for post in valid_posts:
                self.display_post(post)

    def display_post(self, post):
        # Create a frame for each post
        post_frame = tk.Frame(self.scrollable_frame, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Display user name
        user_name_label = tk.Label(post_frame, text=post["user"]["name"], font=("Arial", 12, "bold"),
                                   bg="#ECF0F1", fg="black")
        user_name_label.pack(anchor="w")

        # Display user profile image
        if post["user"].get("profile_image"):
            user_profile_image = Image.open(post["user"]["profile_image"])
            user_profile_image = user_profile_image.resize((30, 30))  # Resize for display
            user_profile_image = ImageTk.PhotoImage(user_profile_image)
            user_profile_image_label = tk.Label(post_frame, image=user_profile_image, bg="#ECF0F1")
            user_profile_image_label.image = user_profile_image  # Keep reference to avoid garbage collection
            user_profile_image_label.pack(side=tk.LEFT, padx=(5, 10))

        # Display post text
        post_label = tk.Label(post_frame, text=post["content"]["text"], font=("Arial", 12), bg="#ECF0F1", fg="black")
        post_label.pack(pady=(0, 10))

        # Display post image if exists
        if post["content"].get("image"):
            post_image = Image.open(post["content"]["image"])
            post_image = post_image.resize((100, 100))
            post_image = ImageTk.PhotoImage(post_image)
            image_label = tk.Label(post_frame, image=post_image, bg="#ECF0F1")
            image_label.image = post_image  # Keep reference to avoid garbage collection
            image_label.pack(pady=5)

        # Display post date
        date_label = tk.Label(post_frame, text=post["content"]["date"], font=("Arial", 8), bg="#ECF0F1", fg="gray")
        date_label.pack(pady=5)

        # Display likes
        likes_label = tk.Label(post_frame, text=f"Likes: {post['content']['likes']}", font=("Arial", 10, "bold"),
                               bg="#ECF0F1", fg="#2980B9")
        likes_label.pack(pady=5)

        # Like button implementation
        like_button = tk.Button(post_frame, text="Like", bg="gray", fg="white",
                                command=lambda: self.toggle_like(post, likes_label))
        like_button.pack(pady=5)

        # Comment section
        comment_frame = tk.Frame(post_frame, bg="#ECF0F1")
        comment_frame.pack(fill=tk.BOTH)

        # Comment entry field
        comment_entry = tk.Entry(comment_frame, font=("Arial", 10), width=40)
        comment_entry.pack(side=tk.LEFT, padx=5)

        comment_button = tk.Button(comment_frame, text="Comment",
                                   command=lambda: self.add_comment(post["id"], comment_entry.get()), bg="#2980B9",
                                   fg="white")
        comment_button.pack(side=tk.LEFT)

        # Display comments
        if post["content"]["comments"]:
            for comment in post["content"]["comments"]:
                comment_label = tk.Label(post_frame, text=comment, font=("Arial", 10), bg="#ECF0F1", fg="black")
                comment_label.pack(anchor="w")

    def add_comment(self, post_id, comment_text):
        if comment_text:
            file_name = "posts.json"
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    data = json.load(f)

                for user_posts in data.get(self.user_email, []):
                    if user_posts["id"] == post_id:
                        user_posts["content"]["comments"].append(comment_text)
                        break

                with open(file_name, 'w') as f:
                    json.dump(data, f, indent=4)

            self.view_posts()  # Refresh the posts after adding a comment
        else:
            print("No comment entered.")

    def toggle_like(self, post, likes_label):
        # Toggle like state
        if post["content"]["likes"] % 2 == 0:  # If currently liked (even number of likes)
            post["content"]["likes"] += 1  # Increment likes
            likes_label.config(text=f"Likes: {post['content']['likes']}")
            likes_label.master.children['!button'].config(bg="blue")  # Change button color to blue
        else:
            post["content"]["likes"] -= 1  # Decrement likes
            likes_label.config(text=f"Likes: {post['content']['likes']}")
            likes_label.master.children['!button'].config(bg="gray")  # Change button color back to gray

        self.save_posts()  # Save updated likes count

    def save_posts(self):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        # Update posts in JSON file
        for user_posts in data.values():
            for post in user_posts:
                # Find and update the post
                if post["id"] == post["id"]:
                    post["content"]["likes"] = post["content"]["likes"]

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)



if __name__ == "__main__":
    root = tk.Tk()
    user_email = {"mail": "test@example.com"}  # Simulating logged in user
    app = Post(root, user_email)
    root.mainloop()
