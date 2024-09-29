import json
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel
from PIL import Image, ImageTk
from datetime import datetime


class Post:

    def __init__(self, root):
        self.root = root
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")

        self.post_text = tk.StringVar()

        profile_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        profile_frame.pack(fill=tk.X, pady=(10, 0))

        self.profile_image_canvas = tk.Canvas(profile_frame, width=50, height=50, bg="#34495E", highlightthickness=0)
        self.profile_image_canvas.grid(row=0, column=0, padx=10)

        self.load_profile_image(r"C:\Users\Abdel\PycharmProjects\sicProj\img\book.jpg")

        name_label = tk.Label(profile_frame, text="Farha Ghallab", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
        name_label.grid(row=0, column=1, sticky='w')

        post_frame = tk.Frame(self.root, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.text_entry = tk.Entry(post_frame, textvariable=self.post_text, font=("Arial", 12), fg="#7F8C8D")
        self.text_entry.insert(0, "Write post here...")
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.config(relief=tk.FLAT, bg="#ECF0F1", highlightbackground="#BDC3C7", highlightthickness=1)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(post_frame, bg="#ECF0F1")
        self.image_label.pack(pady=10)

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

        view_posts_button = tk.Button(self.root, text="View Posts", command=self.view_post_window, bg="#2980B9",
                                      fg="white",
                                      font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        view_posts_button.pack(pady=10)

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
                "likes": 0,
                "liked_by": [],
                "comments": []
            }
            post_data["id"] = self.get_next_post_id()
            self.save_post_to_json(post_data)
            self.root.destroy()
        else:
            print("No text entered for the post.")

    def get_next_post_id(self):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
                max_id = 0
                for user_posts in data.values():
                    for post in user_posts:
                        if post.get('id', 0) > max_id:
                            max_id = post['id']
                return max_id + 1
        return 1

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

        data[user_email].append(post_data)

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Post saved to {file_name}")

    def view_post_window(self):
        view_window = Toplevel(self.root)
        view_window.geometry("600x500")
        view_window.title("View Posts")

        canvas = tk.Canvas(view_window, bg="#ECF0F1")
        canvas.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = tk.Frame(canvas, bg="#ECF0F1")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        posts = self.load_posts_from_json()

        if not posts:
            tk.Label(content_frame, text="No posts available.", bg="#ECF0F1", font=("Arial", 14)).pack(pady=10)
            return

        for post in posts:
            self.display_post(content_frame, post)

    def load_posts_from_json(self):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
            posts = []
            for user_email, user_posts in data.items():
                posts.extend(user_posts)
            return posts
        return []

    def display_post(self, content_frame, post):
        post_frame = tk.Frame(content_frame, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#FFFFFF")
        post_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        post_text = f"{post['content']['text']} - {post['content']['date']}"

        if post['content']['image']:
            try:
                img = Image.open(post['content']['image'])
                img = img.resize((150, 150))
                post_image = ImageTk.PhotoImage(img)
                img_label = tk.Label(post_frame, image=post_image)
                img_label.image = post_image
                img_label.pack()
            except FileNotFoundError:
                tk.Label(post_frame, text="Image not found", font=("Arial", 12), bg="#FFFFFF", fg="red").pack()

        tk.Label(post_frame, text=post_text, font=("Arial", 12), bg="#FFFFFF").pack()
        likes_text = f"Likes: {post.get('likes', 0)}"
        tk.Label(post_frame, text=likes_text, font=("Arial", 12), bg="#FFFFFF").pack()

        like_button = tk.Button(post_frame, text="Like", command=lambda p=post: self.like_post(p),
                                bg="#1ABC9C", fg="white", relief=tk.FLAT, font=("Arial", 12))
        like_button.pack(pady=5)

        comments_label = tk.Label(post_frame, text="Comments:", font=("Arial", 12), bg="#FFFFFF")
        comments_label.pack(pady=5)

        comment_entry = tk.Entry(post_frame, font=("Arial", 12), fg="#7F8C8D")
        comment_entry.insert(0, "Write a comment...")
        comment_entry.pack(pady=5)

        add_comment_button = tk.Button(post_frame, text="Add Comment",
                                       command=lambda p=post, e=comment_entry: self.add_comment(p, e),
                                       bg="#1ABC9C", fg="white", relief=tk.FLAT, font=("Arial", 12))
        add_comment_button.pack(pady=5)

        for comment in post['comments']:
            self.display_comment(post_frame, comment)

    def like_post(self, post):
        user_email = "user@example.com"  # Replace with actual user email
        if user_email in post['liked_by']:
            post['likes'] -= 1
            post['liked_by'].remove(user_email)
        else:
            post['likes'] += 1
            post['liked_by'].append(user_email)

        self.save_post_to_json(post)

    def add_comment(self, post, entry):
        comment_text = entry.get().strip()
        if comment_text and comment_text != "Write a comment...":
            comment = {
                "user": "user@example.com",  # Replace with actual user email
                "content": comment_text,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "likes": 0,
                "liked_by": [],
                "replies": []
            }
            post['comments'].append(comment)
            self.save_post_to_json(post)
            entry.delete(0, tk.END)

    def display_comment(self, post_frame, comment):
        comment_text = f"{comment['user']} - {comment['content']} (Date: {comment['date']}) Likes: {comment['likes']}"
        tk.Label(post_frame, text=comment_text, font=("Arial", 12), bg="#FFFFFF").pack(pady=5)

        like_comment_button = tk.Button(post_frame, text="Like Comment", command=lambda c=comment: self.like_comment(c),
                                        bg="#1ABC9C", fg="white", relief=tk.FLAT, font=("Arial", 12))
        like_comment_button.pack(pady=5)

        reply_button = tk.Button(post_frame, text="Reply", command=lambda c=comment: self.reply_to_comment(c),
                                 bg="#1ABC9C", fg="white", relief=tk.FLAT, font=("Arial", 12))
        reply_button.pack(pady=5)

    def like_comment(self, comment):
        user_email = "user@example.com"  # Replace with actual user email
        if user_email in comment['liked_by']:
            comment['likes'] -= 1
            comment['liked_by'].remove(user_email)
        else:
            comment['likes'] += 1
            comment['liked_by'].append(user_email)

        self.save_post_to_json(comment)

    def reply_to_comment(self, comment):
        reply_text = simpledialog.askstring("Reply", "Enter your reply:")
        if reply_text:
            reply = {
                "user": "user@example.com",  # Replace with actual user email
                "content": reply_text,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "likes": 0,
                "liked_by": []
            }
            comment['replies'].append(reply)
            self.save_post_to_json(comment)

    def save_post_to_json(self, post):
        file_name = "posts.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        user_email = "unknown"

        if user_email in data:
            for p in data[user_email]:
                if p['id'] == post['id']:
                    p.update(post)
                    break
        else:
            data[user_email] = [post]

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def sort_comments_by_likes(self, ascending=True):
        self.comments.sort(key=lambda x: x['likes'], reverse=not ascending)

    def sort_comments_by_date(self, ascending=True):
        self.comments.sort(key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y %H:%M"), reverse=not ascending)


# Run the app
root = tk.Tk()
app = Post(root)
root.mainloop()
