import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime


class Post:

    def __init__(self, root):
        self.root = root
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        self.post_text = tk.StringVar()  # to store the enter text

        profile_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        profile_frame.pack(fill=tk.X)

        self.profile_image_canvas = tk.Canvas(profile_frame, width=50, height=50, bg="#f0f0f0", highlightthickness=0)
        self.profile_image_canvas.grid(row=0, column=0, padx=10)

        self.load_profile_image(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\10 Books That Will Change Your Life - TheFab20s.jpg")

        name_label = tk.Label(profile_frame, text="Farha Ghallab", font=("Helvetica", 14, "bold"), bg="#ffffff")
        name_label.grid(row=0, column=1, sticky='w')

        post_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN, padx=10, pady=10, bg="#ffffff")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)


        self.text_entry = tk.Entry(post_frame, textvariable=self.post_text, font=("Helvetica", 12), fg="gray")
        self.text_entry.insert(0, "Write post here...")  # Default hint text
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = tk.Label(post_frame, bg="#ffffff")
        self.image_label.pack(pady=10)


        icon_frame = tk.Frame(self.root, bg="#ffffff")
        icon_frame.pack(pady=5)


        self.upload_icon = Image.open(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\Camera 01 Icon _ Stroke _ Standard _  Download on Hugeicons Pro.jpg")
        self.upload_icon = self.upload_icon.resize((20, 20))  # Resize photo
        self.upload_icon_photo = ImageTk.PhotoImage(self.upload_icon)

        upload_button = tk.Button(icon_frame, image=self.upload_icon_photo, command=self.upload_image,bg="#ffffff", fg="black", font=("Helvetica", 12), relief=tk.FLAT)
        upload_button.pack(side=tk.LEFT, padx=5)


        post_button = tk.Button(self.root, text="Post", command=self.post_content,bg="#28A745", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        post_button.pack(pady=10)

    def load_profile_image(self, image_path: str):
        img = Image.open(image_path)
        img = img.resize((50, 50))
        self.profile_img = ImageTk.PhotoImage(img)
        self.profile_image_canvas.create_oval(5, 5, 45, 45, outline="gray", width=2)
        self.profile_image_canvas.create_image(25, 25, image=self.profile_img)

    def clear_placeholder(self, event):
        if self.text_entry.get() == "Write post here...":
            self.text_entry.delete(0, tk.END)
            self.text_entry.config(fg="black")  # Change font color to black

    def add_placeholder(self, event):
        if not self.text_entry.get().strip():
            self.text_entry.insert(0, "Write post here...")
            self.text_entry.config(fg="gray")  # Change to gray

    def upload_image(self):
        image_path = filedialog.askopenfilename(title="Select an image",filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            self.display_uploaded_image(image_path)

    def display_uploaded_image(self, image_path):
        uploaded_img = Image.open(image_path)
        uploaded_img = uploaded_img.resize((100, 100))
        self.uploaded_img = ImageTk.PhotoImage(uploaded_img)
        self.image_label.config(image=self.uploaded_img)

    def post_content(self):
        post_text = self.post_text.get().strip()
        if post_text != "" and post_text != "Write post here...":
            print(f"Posted content: {post_text}")
        else:
            print("No text entered for the post.")



root = tk.Tk()
app = Post(root)
root.mainloop()
