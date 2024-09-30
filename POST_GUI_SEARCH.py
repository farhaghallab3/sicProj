import json
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
from datetime import datetime


# def search_accounts_by_name(target_name):
#
#     file_name = 'users.json'
#
#     # Load user data from users.json
#     if os.path.exists(file_name):
#         with open(file_name, 'r') as f:
#             data = json.load(f)
#     else:
#         print(f"Error: {file_name} not found.")
#         return []
#
#     matching_users = []
#
#     # Search through the users based on the first or last name
#     for email, user_info in data.items():
#         full_name = f"{user_info['f name']} {user_info['l name']}"
#
#         if target_name.lower() in user_info['f name'].lower() or target_name.lower() in user_info['l name'].lower():
#             matching_users.append({
#                 "full_name": full_name,
#                 "email": user_info['mail'],
#                 "bio": user_info['bio'],
#                 "job": user_info['job']
#             })
#
#     return matching_users


import tkinter as tk
from datetime import datetime
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import json
import os

class Post:
    def __init__(self, root, user_email):
        self.user_email = user_email.get("mail")
        self.root = root
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")

        self.post_text = tk.StringVar()
        self.uploaded_image_path = None

        profile_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        profile_frame.pack(fill=tk.X, pady=(10, 0))

        self.profile_image_canvas = tk.Canvas(profile_frame, width=50, height=50, bg="#34495E", highlightthickness=0)
        self.profile_image_canvas.grid(row=0, column=0, padx=10)

        self.load_profile_image(r"C:\Users\Abdel\PycharmProjects\sicProj\img\book.jpg")

        self.name_label = tk.Label(profile_frame, text="", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
        self.name_label.grid(row=0, column=1, sticky='w')

        self.post_frame = tk.Frame(self.root, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
        self.post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.text_entry = tk.Entry(self.post_frame, textvariable=self.post_text, font=("Arial", 12), fg="#7F8C8D")
        self.text_entry.insert(0, "Write post here...")
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.config(relief=tk.FLAT, bg="#ECF0F1", highlightbackground="#BDC3C7", highlightthickness=1)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(self.post_frame, bg="#ECF0F1")
        self.image_label.pack(pady=10)

        self.remove_image_button = tk.Button(self.root, text="Remove Image", command=self.remove_image,
                                             bg="#E74C3E", fg="white", font=("Arial", 10), relief=tk.FLAT,
                                             cursor="hand2", borderwidth=0)
        self.remove_image_button.pack(pady=5)
        self.remove_image_button.pack_forget()

        icon_frame = tk.Frame(self.root, bg="#2C3E50")
        icon_frame.pack(pady=5)

        self.upload_icon = Image.open(r"C:\Users\Abdel\PycharmProjects\sicProj\img\camera.jpg")
        self.upload_icon = self.upload_icon.resize((50, 50))
        self.upload_icon_photo = ImageTk.PhotoImage(self.upload_icon)

        upload_button = tk.Button(icon_frame, image=self.upload_icon_photo, command=self.upload_image, bg="#34495E",
                                  fg="white", relief=tk.FLAT, cursor="hand2", borderwidth=0)
        upload_button.pack(side=tk.LEFT, padx=5)

        post_button = tk.Button(self.root, text="Post", command=self.post_content, bg="#1ABC9C", fg="white",
                                font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        post_button.pack(pady=10, ipadx=10, ipady=5)

        self.set_user_profile(user_email)

    def load_profile_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((50, 50), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.profile_image_canvas.create_image(25, 25, image=img)
            self.profile_image_canvas.image = img
        except Exception as e:
            print(f"Error loading image: {e}")

    def set_user_profile(self, user_email):
        user_details = self.get_user_details(user_email)
        self.name_label.config(text=user_details.get("username", "Unknown User"))
        profile_image_path = user_details.get("profile_image", None)
        if profile_image_path:
            self.load_profile_image(profile_image_path)
        else:
            self.load_profile_image(r"C:\Users\Abdel\PycharmProjects\sicProj\img\book.jpg")

    def get_user_details(self, user_email):
        file_name = "users.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
            user_details = next((item for item in data if item["Email"] == user_email["mail"]), {})
            return {
                "username": user_details.get("username", "Unknown User"),
                "profile_image": user_details.get("profile_image", None)
            }
        return {"username": "Unknown User", "profile_image": None}

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
            self.uploaded_image_path = image_path
            self.remove_image_button.pack()

    def display_uploaded_image(self, image_path):
        uploaded_img = Image.open(image_path)
        uploaded_img = uploaded_img.resize((100, 100))
        self.uploaded_img = ImageTk.PhotoImage(uploaded_img)
        self.image_label.config(image=self.uploaded_img)

    def remove_image(self):
        self.image_label.config(image="")
        self.uploaded_image_path = None
        self.remove_image_button.pack_forget()

    def post_content(self):
        post_text = self.post_text.get().strip()
        image_path = getattr(self, 'uploaded_image_path', None)
        user_email = self.user_email

        if post_text and post_text != "Write post here...":
            user_details = self.get_user_details(user_email)
            post_data = {
                "content": {
                    "text": post_text,
                    "image": image_path,
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "likes": 0,
                    "comments": []
                },
                "user": {
                    "username": user_details.get("username", "Unknown User"),
                    "profile_image": user_details.get("profile_image", r"C:\Users\Abdel\PycharmProjects\sicProj\img\book.jpg")
                }
            }
            self.save_post_to_json(post_data, user_email)
            self.view_posts()
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

        post_id = len(data[user_email]) + 1
        post_data["id"] = post_id

        data[user_email].append(post_data)

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def view_posts(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        sort_buttons_frame = tk.Frame(self.root, bg="#34495E")
        sort_buttons_frame.pack(fill=tk.X)

        sort_time_asc_button = tk.Button(sort_buttons_frame, text="Sort by Time Ascending", command=lambda: self.sort_posts_by_time(ascending=True),
                                          bg="#1ABC9C", fg="white", relief=tk.FLAT)
        sort_time_asc_button.pack(side=tk.LEFT, padx=5, pady=5)

        sort_time_desc_button = tk.Button(sort_buttons_frame, text="Sort by Time Descending", command=lambda: self.sort_posts_by_time(ascending=False),
                                           bg="#1ABC9C", fg="white", relief=tk.FLAT)
        sort_time_desc_button.pack(side=tk.LEFT, padx=5, pady=5)

        sort_reactions_button = tk.Button(sort_buttons_frame, text="Sort by Reactions", command=self.sort_posts_by_reactions,
                                          bg="#1ABC9C", fg="white", relief=tk.FLAT)
        sort_reactions_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg="#ECF0F1")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            posts = []
            for user_posts in data.values():
                posts.extend(user_posts)

            valid_posts = [post for post in posts if isinstance(post, dict) and "content" in post and "date" in post["content"]]

            valid_posts.sort(key=lambda x: x["content"]["date"], reverse=True)

            for post in valid_posts:
                self.display_post(post)

    def display_post(self, post):
        post_frame = tk.Frame(self.scrollable_frame, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        post_label = tk.Label(post_frame, text=post["content"]["text"], font=("Arial", 12), bg="#ECF0F1", fg="black")
        post_label.pack(pady=(0, 10))

        if post["content"].get("image"):
            try:
                post_image = Image.open(post["content"]["image"])
                post_image = post_image.resize((100, 100))
                post_image = ImageTk.PhotoImage(post_image)
                image_label = tk.Label(post_frame, image=post_image, bg="#ECF0F1")
                image_label.image = post_image
                image_label.pack(pady=5)
            except FileNotFoundError:
                print("Image file not found.")

        date_label = tk.Label(post_frame, text=post["content"]["date"], font=("Arial", 8), bg="#ECF0F1", fg="gray")
        date_label.pack(pady=5)

        likes_label = tk.Label(post_frame, text=f"Likes: {post['content']['likes']}", font=("Arial", 10, "bold"),
                               bg="#ECF0F1", fg="#2980B9")
        likes_label.pack(pady=5)

        like_button = tk.Button(post_frame, text="Like", bg="gray", fg="white",
                                command=lambda: self.toggle_like(post, likes_label))
        like_button.pack(pady=5)

        comment_frame = tk.Frame(post_frame, bg="#ECF0F1")
        comment_frame.pack(fill=tk.BOTH)

        comment_entry = tk.Entry(comment_frame, font=("Arial", 10), width=40)
        comment_entry.pack(side=tk.LEFT, padx=5)

        comment_button = tk.Button(comment_frame, text="Comment",
                                   command=lambda: self.add_comment(post["id"], comment_entry.get()), bg="#2980B9",
                                   fg="white")
        comment_button.pack(side=tk.LEFT)

        if post["content"]["comments"]:
            for comment in post["content"]["comments"]:
                comment_label = tk.Label(post_frame, text=f"{comment['username']}: {comment['text']} - {comment['date']}",
                                         font=("Arial", 10), bg="#ECF0F1", fg="black")
                comment_label.pack(anchor="w")

                reply_button = tk.Button(post_frame, text="Reply", command=lambda c=comment: self.reply_to_comment(c, post["id"]), bg="#2980B9", fg="white")
                reply_button.pack(anchor="w")

                if 'replies' in comment:
                    for reply in comment['replies']:
                        reply_label = tk.Label(post_frame, text=f"  {reply['username']}: {reply['text']} - {reply['date']}",
                                               font=("Arial", 10), bg="#ECF0F1", fg="gray")
                        reply_label.pack(anchor="w")

    def add_comment(self, post_id, comment_text):
        if comment_text:
            file_name = "posts.json"
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    data = json.load(f)

                for user_posts in data.get(self.user_email, []):
                    if user_posts["id"] == post_id:
                        comment_data = {
                            "username": self.get_user_details(self.user_email)["username"],
                            "text": comment_text,
                            "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                            "likes": 0,
                            "liked_by": [],
                            "replies": []
                        }
                        user_posts["content"]["comments"].append(comment_data)
                        break

                with open(file_name, 'w') as f:
                    json.dump(data, f, indent=4)

            self.view_posts()
        else:
            print("No comment entered.")

    def toggle_like(self, post, likes_label):
        if post["content"]["likes"] % 2 == 0:
            post["content"]["likes"] += 1
            likes_label.config(text=f"Likes: {post['content']['likes']}")
            likes_label.master.children['!button'].config(bg="blue")
        else:
            post["content"]["likes"] -= 1
            likes_label.config(text=f"Likes: {post['content']['likes']}")
            likes_label.master.children['!button'].config(bg="gray")

        self.save_posts()

    def save_posts(self):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        for user_posts in data.values():
            for post in user_posts:
                if post["id"] == post["id"]:
                    post["content"]["likes"] = post["content"]["likes"]

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def reply_to_comment(self, comment, post_id):
        reply_text = simpledialog.askstring("Reply", "Enter your reply:")
        if reply_text:
            reply = {
                "username": self.get_user_details(self.user_email)["username"],
                "text": reply_text,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            }
            comment['replies'].append(reply)
            self.save_posts()
            self.view_posts()

    def sort_posts_by_time(self, ascending=True):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            all_posts = []
            for user_posts in data.values():
                all_posts.extend(user_posts)

            sorted_posts = sorted(all_posts, key=lambda x: x['content']['date'], reverse=not ascending)

            self.display_sorted_posts(sorted_posts)

    def sort_posts_by_reactions(self):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)

            all_posts = []
            for user_posts in data.values():
                all_posts.extend(user_posts)

            sorted_posts = sorted(all_posts, key=lambda x: x['content']['likes'], reverse=True)

            self.display_sorted_posts(sorted_posts)

    def display_sorted_posts(self, sorted_posts):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for post in sorted_posts:
            self.display_post(post)


if __name__ == "__main__":
    root = tk.Tk()
    user_email = {"mail": "test@example.com"}
    app = Post(root, user_email)
    root.mainloop()
