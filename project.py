import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime


class Post:

    def __init__(self, root):
        self.root = root
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")  # Dark background for a modern look

        self.post_text = tk.StringVar()  # To store the entered text

        # Profile frame setup
        profile_frame = tk.Frame(self.root, bg="#34495E", padx=10, pady=10)
        profile_frame.pack(fill=tk.X, pady=(10, 0))

        # Profile image canvas with a circular profile
        self.profile_image_canvas = tk.Canvas(profile_frame, width=50, height=50, bg="#34495E", highlightthickness=0)
        self.profile_image_canvas.grid(row=0, column=0, padx=10)

        self.load_profile_image(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\10 Books That Will Change Your Life - TheFab20s.jpg")

        # Profile name label with new font style and color
        name_label = tk.Label(profile_frame, text="Farha Ghallab", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
        name_label.grid(row=0, column=1, sticky='w')

        # Post frame for entering post content
        post_frame = tk.Frame(self.root, bd=2, relief=tk.FLAT, padx=10, pady=10, bg="#ECF0F1")
        post_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Text entry for post content
        self.text_entry = tk.Entry(post_frame, textvariable=self.post_text, font=("Arial", 12), fg="#7F8C8D")
        self.text_entry.insert(0, "Write post here...")  # Default hint text
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.add_placeholder)
        self.text_entry.config(relief=tk.FLAT, bg="#ECF0F1", highlightbackground="#BDC3C7", highlightthickness=1)
        self.text_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Label for displaying uploaded images
        self.image_label = tk.Label(post_frame, bg="#ECF0F1")
        self.image_label.pack(pady=10)

        # Frame for upload and post buttons
        icon_frame = tk.Frame(self.root, bg="#2C3E50")
        icon_frame.pack(pady=5)

        # Upload icon button
        self.upload_icon = Image.open(r"C:\Users\farha\OneDrive\Desktop\sicProj\img\Camera 01 Icon _ Stroke _ Standard _  Download on Hugeicons Pro.jpg")
        self.upload_icon = self.upload_icon.resize((50, 50))  # Resize photo
        self.upload_icon_photo = ImageTk.PhotoImage(self.upload_icon)

        upload_button = tk.Button(icon_frame, image=self.upload_icon_photo, command=self.upload_image, bg="#34495E",
                                  fg="white", relief=tk.FLAT, cursor="hand2", borderwidth=0)
        upload_button.pack(side=tk.LEFT, padx=5)

        # Post button with modern green color
        post_button = tk.Button(self.root, text="Post", command=self.post_content, bg="#1ABC9C", fg="white",
                                font=("Arial", 12), relief=tk.FLAT, cursor="hand2", borderwidth=0)
        post_button.pack(pady=10, ipadx=10, ipady=5)

    # Load profile image and display it as circular
    def load_profile_image(self, image_path: str):
        img = Image.open(image_path)
        img = img.resize((50, 50))
        self.profile_img = ImageTk.PhotoImage(img)
        self.profile_image_canvas.create_oval(5, 5, 45, 45, outline="#1ABC9C", width=2)
        self.profile_image_canvas.create_image(25, 25, image=self.profile_img)

    # Clear placeholder on focus in
    def clear_placeholder(self, event):
        if self.text_entry.get() == "Write post here...":
            self.text_entry.delete(0, tk.END)
            self.text_entry.config(fg="black")  # Change font color to black

    # Add placeholder on focus out
    def add_placeholder(self, event):
        if not self.text_entry.get().strip():
            self.text_entry.insert(0, "Write post here...")
            self.text_entry.config(fg="#7F8C8D")  # Change to gray

    # Open file dialog to upload image
    def upload_image(self):
        image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            self.display_uploaded_image(image_path)

    # Display uploaded image in the post
    def display_uploaded_image(self, image_path):
        uploaded_img = Image.open(image_path)
        uploaded_img = uploaded_img.resize((100, 100))
        self.uploaded_img = ImageTk.PhotoImage(uploaded_img)
        self.image_label.config(image=self.uploaded_img)

    # Post content logic
    def post_content(self):
        post_text = self.post_text.get().strip()
        if post_text != "" and post_text != "Write post here...":
            print(f"Posted content: {post_text}")
        else:
            print("No text entered for the post.")


# Initialize the Tkinter root and run the application
root = tk.Tk()
app = Post(root)
root.mainloop()
