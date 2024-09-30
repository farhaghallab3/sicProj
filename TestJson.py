import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import json

# Function to load and resize an image
def load_image(image_path, size=(60, 60)):
    try:
        img = Image.open(image_path).resize(size, Image.LANCZOS)  # Use LANCZOS for quality
        return img
    except Exception as e:
        print("Error loading image:", e)
        return None

class HomePageApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight() - 40  # Adjust for taskbar height

        # Set the window size
        self.geometry(f"{screen_width}x{screen_height}")
        self.resizable(False, False)

        # Set top and bottom distance
        top_distance = 100
        bottom_distance = 30

        # Calculate the available height for the frame
        available_height = screen_height - top_distance - bottom_distance

        # Create a main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.place(x=0, y=top_distance, relwidth=1, height=available_height)

        # Create a canvas inside the main frame
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.canvas_width = 800  # Set a width for the canvas
        self.canvas_height = available_height  # Use the available height

        # Place the canvas at the center
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=self.canvas_width, height=self.canvas_height)

        # Add a scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(relx=1, rely=0, anchor="ne", height=self.canvas_height)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a scrollable frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((200, 0), window=self.scrollable_frame, anchor="nw")

        # Initialize the frames for friend posts
        self.view_friends_posts = ViewFriendsPosts(self.scrollable_frame, self, "ahmed.ibrahim@gmail.com")

        # Show the friend posts by default
        self.show_frame(self.view_friends_posts)

    def show_frame(self, frame):
        """Hide the current frame and show the specified frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()  # Clear current contents
        frame.pack(fill="both", expand=True)  # Pack the new frame


class ViewFriendsPosts(tk.Frame):
    def __init__(self, parent, app, user_email, total_posts=100):
        super().__init__(parent)

        self.user_email = user_email
        self.total_posts = total_posts

        # Dummy data for friends and posts
        self.friends, self.posts = self.load_posts()

        # Initialize display variables
        self.displayed_posts = 0
        self.current_friend_idx = 0
        self.profile_photo = "path/to/default_profile_image.png"  # Set to valid image path

        self.load_and_display_posts()

    def load_posts(self):
        # Placeholder for loading posts; adapt this to actual post loading logic
        return {}, {}

    def load_and_display_posts(self):
        """Load posts and display them using logic from the first code block."""
        # Clear existing posts
        for widget in self.winfo_children():
            widget.destroy()

        friend_keys = list(self.friends.keys())
        while self.displayed_posts < self.total_posts and self.current_friend_idx < len(friend_keys):
            friend = friend_keys[self.current_friend_idx]

            for post in self.posts[friend]:
                # Display the post using the first code's GUI logic
                self.display_post(post)

                # Increment displayed post count
                self.displayed_posts += 1

            # Move to the next friend
            self.current_friend_idx += 1

            # Reset to first friend if end of list is reached
            if self.current_friend_idx >= len(friend_keys):
                self.current_friend_idx = 0

        # Add "View More" button if more posts need to be shown
        if self.displayed_posts < self.total_posts:
            view_more_button = tk.Button(self, text="View More Posts", command=self.load_and_display_posts)
            view_more_button.pack(pady=10)

    def display_post(self, post):
        """This function will implement the logic from the first code block for displaying each post."""
        post_frame = tk.Frame(self, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Display the post content
        post_label = tk.Label(post_frame, text=post["content"]["text"], font=("Arial", 12), bg="#ECF0F1", fg="black")
        post_label.pack(pady=(0, 10))

        # Display post image if available
        if post["content"].get("image"):
            try:
                post_image = Image.open(post["content"]["image"])
                post_image = post_image.resize((100, 100))
                post_image = ImageTk.PhotoImage(post_image)
                image_label = tk.Label(post_frame, image=post_image, bg="#ECF0F1")
                image_label.image = post_image  # Keep reference to avoid garbage collection
                image_label.pack(pady=5)
            except FileNotFoundError:
                print("Image file not found.")

        # Display date
        date_label = tk.Label(post_frame, text=post["content"]["date"], font=("Arial", 8), bg="#ECF0F1", fg="gray")
        date_label.pack(pady=5)

        # Likes and Like button
        likes_label = tk.Label(post_frame, text=f"Likes: {post['content']['likes']}", font=("Arial", 10, "bold"),
                               bg="#ECF0F1", fg="#2980B9")
        likes_label.pack(pady=5)

        like_button = tk.Button(post_frame, text="Like", bg="gray", fg="white",
                                command=lambda: self.toggle_like(post, likes_label))
        like_button.pack(pady=5)

        # Display comments, if any
        if post["content"]["comments"]:
            for comment in post["content"]["comments"]:
                comment_label = tk.Label(post_frame, text=f"{comment['username']}: {comment['text']} - {comment['date']}",
                                         font=("Arial", 10), bg="#ECF0F1", fg="black")
                comment_label.pack(anchor="w")

                # Reply button
                reply_button = tk.Button(post_frame, text="Reply", command=lambda c=comment: self.reply_to_comment(c, post["id"]), bg="#2980B9", fg="white")
                reply_button.pack(anchor="w")

                if 'replies' in comment:
                    for reply in comment['replies']:
                        reply_label = tk.Label(post_frame, text=f"  {reply['username']}: {reply['text']} - {reply['date']}",
                                               font=("Arial", 10), bg="#ECF0F1", fg="gray")
                        reply_label.pack(anchor="w")

    def toggle_like(self, post, likes_label):
        # Logic for toggling like (from first code)
        post["content"]["likes"] += 1
        likes_label.config(text=f"Likes: {post['content']['likes']}")

    def reply_to_comment(self, comment, post_id):
        # Logic for replying to a comment (from first code)
        reply_text = tk.simpledialog.askstring("Reply", "Enter your reply:")
        if reply_text:
            reply = {
                "username": "YourUsername",  # Replace with actual username
                "text": reply_text,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            }
            comment['replies'].append(reply)
            self.load_and_display_posts()  # Refresh posts


# Function to scroll with the mouse wheel
def on_mouse_wheel(event):
    app.canvas.yview_scroll(-1 * (event.delta // 120), "units")


# Create the application instance
app = HomePageApp()

# Bind mouse wheel scrolling
app.bind_all("<MouseWheel>", on_mouse_wheel)

# Start the application
app.mainloop()
