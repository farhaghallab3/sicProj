import json
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image as PilImage, ImageTk
from datetime import datetime

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
max_width = min(1366, screen_width)
max_height = min(768, screen_height)
width, height = max_width, max_height
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack(fill="both", expand=True)
root.resizable(False, False)

class Post:
    def __init__(self, post_main):
        self.post_main = post_main
        self.post_main.geometry("500x600")
        self.post_main.configure(bg="#2C3E50")
        self.likes = 0
        self.liked_by = []
        self.comments = []

        self.post_text = tk.StringVar()  # To store the entered text
        self.comment_text = tk.StringVar()  # To store the comment text

        # Profile frame setup
        profile_frame = tk.Frame(self.post_main, bg="#34495E", padx=10, pady=10)
        profile_frame.pack(fill=tk.X, pady=(10, 0))

        # Profile image label
        self.profile_img_label = tk.Label(profile_frame, bg="#34495E")
        self.profile_img_label.grid(row=0, column=0, padx=10)

        # Load profile image with corrected path
        self.load_profile_image(r"C:\Users\Lenovo\Downloads\5480.jpg")

        # Profile name label with new font style and color
        name_label = tk.Label(profile_frame, text="Farha Ghallab", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
        name_label.grid(row=0, column=1, sticky='w')

        post_frame = tk.Frame(self.post_main, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Post text entry
        self.text_entry = tk.Entry(post_frame, textvariable=self.post_text, font=("Arial", 12), fg="#7F8C8D")
        self.text_entry.insert(0, "Write post here...")  # Default hint text
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.config(relief=tk.FLAT, bg="#ECF0F1", highlightbackground="#BDC3C7", highlightthickness=1)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(post_frame, bg="#ECF0F1")
        self.image_label.pack(pady=10)

        icon_frame = tk.Frame(self.post_main, bg="#2C3E50")
        icon_frame.pack(pady=5)

        self.upload_icon = PilImage.open(r"C:\Users\Lenovo\Downloads\negotiation-strategies.jpeg")
        self.upload_icon = self.upload_icon.resize((50, 50))  # Resize photo
        self.upload_icon_photo = ImageTk.PhotoImage(self.upload_icon)

        upload_button = tk.Button(icon_frame, image=self.upload_icon_photo, command=self.upload_image, bg="#34495E",
                                  fg="white", relief=tk.FLAT, cursor="hand2", borderwidth=0)
        upload_button.pack(side=tk.LEFT, padx=5)

        post_button = tk.Button(self.post_main, text="Post", command=self.post_content, bg="#1ABC9C", fg="white",
                                font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        post_button.pack(pady=10, ipadx=10, ipady=5)

        # Likes Display
        self.likes_label = tk.Label(self.post_main, text="Likes: 0", font=("Arial", 12), bg="#2C3E50", fg="white")
        self.likes_label.pack(pady=10)

        like_button = tk.Button(self.post_main, text="Like", command=lambda: self.like("user@example.com"),
                                bg="#1ABC9C", fg="white", font=("Arial", 12), relief=tk.FLAT, cursor="hand2",
                                borderwidth=0)
        like_button.pack(pady=5)

        # Comments Section
        comments_label = tk.Label(self.post_main, text="Comments:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white")
        comments_label.pack(pady=10)

        self.comment_entry = tk.Entry(self.post_main, textvariable=self.comment_text, font=("Arial", 12), fg="#7F8C8D")
        self.comment_entry.insert(0, "Write a comment...")  # Default hint text
        self.comment_entry.bind("<FocusIn>", self.clear_comment_placeholder)
        self.comment_entry.bind("<FocusOut>", self.add_comment_placeholder)
        self.comment_entry.pack(fill=tk.BOTH, padx=10, pady=5)

        comment_button = tk.Button(self.post_main, text="Add Comment", command=self.add_comment, bg="#1ABC9C", fg="white",
                                   font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        comment_button.pack(pady=5)

        self.comments_display = tk.Frame(self.post_main, bg="#ECF0F1")
        self.comments_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Buttons to sort comments
        sort_frame = tk.Frame(self.post_main, bg="#2C3E50")
        sort_frame.pack(pady=5)

        sort_likes_button = tk.Button(sort_frame, text="Sort Comments by Likes", command=self.sort_comments_by_likes,
                                      bg="#1ABC9C", fg="white", font=("Arial", 12), relief=tk.FLAT, cursor="hand2",
                                      borderwidth=0)
        sort_likes_button.pack(side=tk.LEFT, padx=5)

        sort_date_button = tk.Button(sort_frame, text="Sort Comments by Date", command=self.sort_comments_by_date,
                                     bg="#1ABC9C", fg="white", font=("Arial", 12), relief=tk.FLAT, cursor="hand2",
                                     borderwidth=0)
        sort_date_button.pack(side=tk.LEFT, padx=5)

    def load_profile_image(self, image_path: str):
        img = PilImage.open(image_path)
        img = img.resize((50, 50))
        self.profile_img = ImageTk.PhotoImage(img)
        self.profile_img_label.config(image=self.profile_img)
        self.profile_img_label.image = self.profile_img

    def clear_placeholder(self, event):
        if self.text_entry.get() == "Write post here...":
            self.text_entry.delete(0, tk.END)
            self.text_entry.config(fg="black")  #

    def add_placeholder(self, event):
        if not self.text_entry.get().strip():
            self.text_entry.insert(0, "Write post here...")
            self.text_entry.config(fg="#7F8C8D")

    def clear_comment_placeholder(self, event):
        if self.comment_entry.get() == "Write a comment...":
            self.comment_entry.delete(0, tk.END)
            self.comment_entry.config(fg="black")

    def add_comment_placeholder(self, event):
        if not self.comment_entry.get().strip():
            self.comment_entry.insert(0, "Write a comment...")
            self.comment_entry.config(fg="#7F8C8D")

    def upload_image(self):
        image_path = filedialog.askopenfilename(title="Select an image",
                                                filetypes=[("Image files", ".png;.jpg;*.jpeg")])
        if image_path:
            self.display_uploaded_image(image_path)
            self.uploaded_image_path = image_path

    def display_uploaded_image(self, image_path):
        uploaded_img = PilImage.open(image_path)
        uploaded_img = uploaded_img.resize((100, 100))
        self.uploaded_img = ImageTk.PhotoImage(uploaded_img)
        self.image_label.config(image=self.uploaded_img)

    def post_content(self):
        post_text = self.post_text.get().strip()
        image_path = getattr(self, 'uploaded_image_path', None)
        if post_text and post_text != "Write post here...":
            post_data = {
                "content": {
                    "text": post_text,
                    "image": image_path,
                    "date": datetime.now().strftime("%d-%m-%Y"),
                },
                "likes": self.likes,
                "liked_by": self.liked_by,
                "comments": self.comments,
            }
            self.save_post_to_json(post_data)
        else:
            l1 = tk.Label(self.post_main, text="No text entered for the post.")
            l1.pack(pady=10)
            def hide_label():
                l1.config(text="")
            self.post_main.after(3000, hide_label)

    def save_post_to_json(self, post_data):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        user_email = "unknown"

        if user_email not in data:
            data[user_email] = []

        post_id = len(data[user_email]) + 1
        post_data["id"] = post_id

        data[user_email].append(post_data)

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        l1 = tk.Label(self.post_main, text="Post saved Successfully.")
        l1.pack(pady=10)
        def hide_label():
            l1.config(text="")
        self.post_main.after(3000, hide_label)

    def like(self, user_email):
        """Like or unlike the post based on the user's previous action."""
        if user_email in self.liked_by:
            self.likes -= 1
            self.liked_by.remove(user_email)
            # print(f"{user_email} unliked the post.")
        else:
            self.likes += 1
            self.liked_by.append(user_email)
            # print(f"{user_email} liked the post.")
        self.likes_label.config(text=f"Likes: {self.likes}")

    def add_comment(self):
        comment_text = self.comment_text.get().strip()
        if comment_text and comment_text != "Write a comment...":
            comment_data = {
                "text": comment_text,
                "date": datetime.now().strftime("%d-%m-%Y"),
                "likes": 0
            }
            self.comments.append(comment_data)
            self.display_comments()
        else:
            print("No comment entered.")

    def display_comments(self):
        for widget in self.comments_display.winfo_children():
            widget.destroy()

        for comment in self.comments:
            comment_label = tk.Label(self.comments_display, text=comment["text"], font=("Arial", 12), bg="#ECF0F1",
                                     fg="black")
            comment_label.pack(anchor="w", pady=2)

            like_comment_button = tk.Button(self.comments_display, text=f"Like ({comment['likes']})",
                                            command=lambda c=comment: self.like_comment(c), bg="#1ABC9C", fg="white",
                                            font=("Arial", 10), relief=tk.FLAT, cursor="hand2", borderwidth=0)
            like_comment_button.pack(anchor="w", pady=2)

    def like_comment(self, comment):
        comment["likes"] += 1
        self.display_comments()

    def sort_comments_by_likes(self):
        self.comments.sort(key=lambda c: c['likes'], reverse=True)
        self.display_comments()

    def sort_comments_by_date(self):
        self.comments.sort(key=lambda c: datetime.strptime(c['date'], "%d-%m-%Y"), reverse=True)
        self.display_comments()

def call_post_main():
    post_main = tk.Toplevel(root)
    app = Post(post_main)
    post_main.mainloop()


class HomePage:
    def __init__(self):
        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Configure button properties
        add_p_btn = tk.Button(
            root,
            text="Add Post",
            command=call_post_main,
            font=("Arial", 16, "bold"),  # Slightly smaller font size
            bg="#4267B2",  # Facebook-like blue color
            fg="white",  # Button text color
            activebackground="#365899",  # Darker blue when pressed
            activeforeground="white",  # Text color when pressed
            relief=tk.RAISED,  # Button style (raised appearance)
            bd=3  # Slightly thinner border
        )

        # Adjusted button size: slightly smaller than before
        button_width = screen_width // 8  # Slightly smaller width
        button_height = screen_height // 18  # Slightly smaller height

        # Use `place()` to center the button horizontally and place it slightly below the top
        add_p_btn.place(
            x=(screen_width - button_width) // 2,  # Center horizontally
            y=screen_height // 8,  # Near the top but at medium distance (1/8th from top)
            width=button_width,  # Button width in pixels
            height=button_height  # Button height in pixels
        )






homeP = HomePage()
root.mainloop()