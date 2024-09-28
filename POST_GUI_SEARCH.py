import json
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
from datetime import datetime


class Post:
    def _init_(self, root):
        self.root = root
        self.root.geometry("500x600")
        self.root.configure(bg="#2C3E50")
        self.likes = 0
        self.liked_by = []
        self.comments = []

        self.post_text = tk.StringVar()  # To store the entered text
        self.comment_text = tk.StringVar()  # To store the comment text

        # Profile frame setup
        profile_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        profile_frame.pack(fill=tk.X, pady=(10, 0))

        # Profile image label
        self.profile_img_label = tk.Label(profile_frame, bg="#34495E")
        self.profile_img_label.grid(row=0, column=0, padx=10)

        # Load profile image with corrected path
        self.load_profile_image(r"C:\Users\Abdel\PycharmProjects\sicProj\img\book.jpg")

        # Profile name label with new font style and color
        name_label = tk.Label(profile_frame, text="Farha Ghallab", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
        name_label.grid(row=0, column=1, sticky='w')

        post_frame = tk.Frame(self.root, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
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

        icon_frame = tk.Frame(self.root, bg="#2C3E50")
        icon_frame.pack(pady=5)

        self.upload_icon = Image.open(r"C:\Users\Abdel\PycharmProjects\sicProj\img\camera.jpg")
        self.upload_icon = self.upload_icon.resize((50, 50))  # Resize photo
        self.upload_icon_photo = ImageTk.PhotoImage(self.upload_icon)

        upload_button = tk.Button(icon_frame, image=self.upload_icon_photo, command=self.upload_image, bg="#34495E",
                                  fg="white", relief=tk.FLAT, cursor="hand2", borderwidth=0)
        upload_button.pack(side=tk.LEFT, padx=5)

        post_button = tk.Button(self.root, text="Post", command=self.post_content, bg="#1ABC9C", fg="white",
                                font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        post_button.pack(pady=10, ipadx=10, ipady=5)

        # Likes Display
        self.likes_label = tk.Label(self.root, text="Likes: 0", font=("Arial", 12), bg="#2C3E50", fg="white")
        self.likes_label.pack(pady=10)

        like_button = tk.Button(self.root, text="Like", command=lambda: self.like("user@example.com"),
                                bg="#1ABC9C", fg="white", font=("Arial", 12), relief=tk.FLAT, cursor="hand2",
                                borderwidth=0)
        like_button.pack(pady=5)

        # Comments Section
        comments_label = tk.Label(self.root, text="Comments:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white")
        comments_label.pack(pady=10)

        self.comment_entry = tk.Entry(self.root, textvariable=self.comment_text, font=("Arial", 12), fg="#7F8C8D")
        self.comment_entry.insert(0, "Write a comment...")  # Default hint text
        self.comment_entry.bind("<FocusIn>", self.clear_comment_placeholder)
        self.comment_entry.bind("<FocusOut>", self.add_comment_placeholder)
        self.comment_entry.pack(fill=tk.BOTH, padx=10, pady=5)

        comment_button = tk.Button(self.root, text="Add Comment", command=self.add_comment, bg="#1ABC9C", fg="white",
                                   font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        comment_button.pack(pady=5)

        self.comments_display = tk.Frame(self.root, bg="#ECF0F1")
        self.comments_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Buttons to sort comments
        sort_frame = tk.Frame(self.root, bg="#2C3E50")
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
        img = Image.open(image_path)
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
        uploaded_img = Image.open(image_path)
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
            print("No text entered for the post.")

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

        print(f"Post saved to {file_name}")


    def like(self, user_email):
        """Like or unlike the post based on the user's previous action."""
        if user_email in self.liked_by:
            self.likes -= 1
            self.liked_by.remove(user_email)
            print(f"{user_email} unliked the post.")
        else:
            self.likes += 1
            self.liked_by.append(user_email)
            print(f"{user_email} liked the post.")

        # Update likes label in GUI
        self.likes_label.config(text=f"Likes: {self.likes}")



    def add_comment(self):
        """Add a comment to the post."""
        comment_text = self.comment_text.get().strip()  # Get comment text
        if comment_text and comment_text != "Write a comment...":
            user_email = "user@example.com"  # Replace with the actual user email
            comment = {
                "user": user_email,
                "content": {
                    "text": comment_text,
                    "date": datetime.now().strftime("%d-%m-%Y")
                },
                "likes": 0,
                "liked_by": [],
                "replies": []  # Initialize replies for nested comments
            }
            self.comments.append(comment)
            print(f"Comment by {user_email} added: {comment_text}")
            self.save_comments_to_json()  # Save comments to JSON
            self.update_comments_display()  # Update the GUI to show the new comment
            self.comment_entry.delete(0, tk.END)  # Clear the comment entry field
        else:
            print("No text entered for the comment.")

    def save_comments_to_json(self):

        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        user_email = "unknown"
        post_id = 1

        if user_email in data:
            for post in data[user_email]:
                if post['id'] == post_id:  # Find the specific post
                    post['comments'] = self.comments
                    break

        # Write updated data back to the JSON
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Comments updated in {file_name}")

    def update_comments_display(self):

        # Clear current display
        for widget in self.comments_display.winfo_children():
            widget.destroy()

        for comment in self.comments:

            comment_frame = tk.Frame(self.comments_display, bg="#ECF0F1")
            comment_frame.pack(fill=tk.X)


            comment_display = f"{comment['user']} - {comment['content']['text']} (Date: {comment['content']['date']}) Likes: {comment['likes']}"


            label = tk.Label(comment_frame, text=comment_display, bg="#ECF0F1")
            label.pack(side=tk.LEFT, padx=5)


            like_button = tk.Button(comment_frame, text="Like", command=lambda c=comment: self.like_comment(c),
                                    bg="#1ABC9C", fg="white")
            like_button.pack(side=tk.LEFT, padx=5)

            # Create reply button for each comment
            reply_button = tk.Button(comment_frame, text="Reply", command=lambda c=comment: self.reply_to_comment(c),
                                     bg="#1ABC9C", fg="white")
            reply_button.pack(side=tk.LEFT, padx=5)

            # Display replies if any
            for reply in comment['replies']:
                reply_frame = tk.Frame(comment_frame, bg="#ECF0F1")
                reply_frame.pack(fill=tk.X, padx=(20, 0))  # Indent replies

                reply_display = f"   Reply from {reply['user']}: {reply['content']['text']} (Date: {reply['content']['date']}) Likes: {reply['likes']}"
                reply_label = tk.Label(reply_frame, text=reply_display, bg="#ECF0F1")
                reply_label.pack(side=tk.LEFT, padx=5)

                # Create like button for each reply
                reply_like_button = tk.Button(reply_frame, text="Like", command=lambda r=reply: self.like_reply(r),
                                              bg="#1ABC9C", fg="white")
                reply_like_button.pack(side=tk.LEFT, padx=5)

                # Create reply button for each reply
                reply_reply_button = tk.Button(reply_frame, text="Reply",
                                               command=lambda r=reply: self.reply_to_reply(r), bg="#1ABC9C", fg="white")
                reply_reply_button.pack(side=tk.LEFT, padx=5)



    def like_comment(self, comment):
        """Like or unlike a specific comment."""
        if comment in self.liked_by:
            comment['likes'] -= 1
            comment['liked_by'].remove("user@example.com")
            print(f"{comment['user']} unliked the comment.")
        else:
            comment['likes'] += 1
            comment['liked_by'].append("user@example.com")
            print(f"{comment['user']} liked the comment.")

        self.update_comments_display()

    def reply_to_comment(self, comment):
        """Prompt for reply text and add it to the specified comment."""
        reply_text = simpledialog.askstring("Reply", "Enter your reply:")
        if reply_text:
            reply = {
                "user": "user@example.com",
                "content": {
                    "text": reply_text,
                    "date": datetime.now().strftime("%d-%m-%Y"),
                },
                "likes": 0,
                "liked_by": [],
                "replies": []
            }
            comment['replies'].append(reply)
            print(f"Reply added to comment by {comment['user']}.")

            self.save_comments_to_json()
            self.update_comments_display()

    def like_reply(self, reply):
        """Like or unlike a specific reply."""
        if reply in self.liked_by:
            reply['likes'] -= 1
            reply['liked_by'].remove("user@example.com")
            print(f"{reply['user']} unliked the reply.")
        else:
            reply['likes'] += 1
            reply['liked_by'].append("user@example.com")
            print(f"{reply['user']} liked the reply.")

        self.update_comments_display()

    def reply_to_reply(self, reply):
        """Prompt for reply text and add it to the specified reply."""
        reply_text = simpledialog.askstring("Reply", "Enter your reply:")
        if reply_text:
            reply_reply = {
                "user": "user@example.com",
                "content": {
                    "text": reply_text,
                    "date": datetime.now().strftime("%d-%m-%Y"),
                },
                "likes": 0,
                "liked_by": []
            }

            if 'replies' not in reply:
                reply['replies'] = []

            reply['replies'].append(reply_reply)
            print(f"Reply added to reply by {reply['user']}.")

            self.save_comments_to_json()
            self.update_comments_display()

    def sort_comments_by_likes(self, ascending=True):
        """Sort comments based on the number of likes."""
        self.comments.sort(key=lambda x: x['likes'], reverse=not ascending)
        print(f"Comments sorted by likes in {'ascending' if ascending else 'descending'} order.")
        self.update_comments_display()

    def sort_comments_by_date(self, ascending=True):
        self.comments.sort(key=lambda x: datetime.strptime(x['content']['date'], "%d-%m-%Y"), reverse=not ascending)
        print(f"Comments sorted by date in {'ascending' if ascending else 'descending'} order.")
        self.update_comments_display()


# Run the app
root = tk.Tk()
app = Post(root)
root.mainloop()