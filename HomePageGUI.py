import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from NewsFeedLogic import view_post, friend_posts_read
from POST_GUI_SEARCH import Post

temp_idx = -1

# Function to load and resize an image
def load_image(image_path, size=(60, 60)):
    try:
        img = Image.open(image_path).resize(size, Image.LANCZOS)  # Use LANCZOS for quality
        return img
    except Exception as e:
        print("Error loading image:", e)
        return None


# Create the main window
class HomePageApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Get screen dimensions, excluding taskbar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight() - 40  # Adjust for taskbar height

        # Set the window size to fill the screen except for the taskbar
        self.geometry(f"{screen_width}x{screen_height}")

        # Make the window non-resizable
        self.resizable(False, False)

        # Set fixed distances from the top and bottom
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
        self.view_friends_posts = View_Friends_Posts(self.scrollable_frame, self, "ahmed.ibrahim@gmail.com", temp_idx)

        # Show the incoming requests frame by default
        self.show_frame(self.view_friends_posts)


    def show_frame(self, frame):
        """Hide the current frame and show the specified frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()  # Clear current contents
        frame.pack(fill="both", expand=True)  # Pack the new frame


class View_Friends_Posts(tk.Frame):
    def __init__(self, parent, app, mail, start_idx=-1, total_posts=100):
        super().__init__(parent)

        self.mail = mail
        self.start_idx = start_idx
        self.total_posts = total_posts
        self.friends, self.posts = friend_posts_read()

        # Initialize display variables
        self.displayed_posts = 0
        self.current_friend_idx = 0
        self.profile_photo = "path/to/default_profile_image.png"  # Change to a valid path

        self.load_posts()

    def load_posts(self):
        # Clear existing posts if any
        for widget in self.winfo_children():
            widget.destroy()

        # Loop through friends and display posts
        friend_keys = list(self.friends[self.mail]["friends"])
        while self.displayed_posts < self.total_posts and self.current_friend_idx < len(friend_keys):
            friend = friend_keys[self.current_friend_idx]
            # Display up to 2 posts for the current friend
            for _ in range(2):
                if self.displayed_posts >= self.total_posts:
                    break  # Stop if we've displayed enough posts

                # Calculate the index for older posts
                post_idx = -1 - (self.displayed_posts % len(self.posts[friend]))

                # Check if there are enough posts
                if abs(post_idx) > len(self.posts[friend]):
                    continue  # No more posts to show for this friend

                # Get the current post for the friend
                post = self.posts[friend][post_idx]

                # Create a frame for each post
                request_frame = tk.Frame(self, bd=2, relief=tk.RAISED, padx=10, pady=10, width=300)
                request_frame.pack(fill="x", pady=5, padx=20)

                # Load and display the profile photo
                img = load_image(self.profile_photo)
                if img:
                    img_tk = ImageTk.PhotoImage(img)
                    photo_label = tk.Label(request_frame, image=img_tk)
                    photo_label.image = img_tk  # Keep a reference
                    photo_label.grid(row=0, column=0, padx=5, pady=5)

                # Create a frame for the text details
                details_frame = tk.Frame(request_frame)
                details_frame.grid(row=0, column=1, padx=10, sticky="w")

                # Display the post content
                name_label = tk.Label(details_frame, text=post["content"]["text"], font=("Helvetica", 12, "bold"))
                name_label.pack(anchor="w")

                # Display the number of likes or other reactions
                random_param_label = tk.Label(details_frame, text=post["reactions"]["likes"], font=("Helvetica", 10))
                random_param_label.pack(anchor="w")

                # Add buttons for accepting and declining the post
                button_frame = tk.Frame(request_frame)
                button_frame.grid(row=0, column=2, sticky="e")

                # Create Accept button
                accept_button = tk.Button(button_frame, text="Accept")
                accept_button.pack(side="top", padx=5, pady=2)

                # Create Decline button
                decline_button = tk.Button(button_frame, text="Decline")
                decline_button.pack(side="top", padx=5, pady=2)

                # Update displayed posts count
                self.displayed_posts += 1

            # Move to the next friend
            self.current_friend_idx += 1

            # Reset to the first friend if we reach the end
            if self.current_friend_idx >= len(friend_keys):
                self.current_friend_idx = 0

        # Optional: Add a "View More Posts" button if needed
        if self.displayed_posts < self.total_posts:
            view_more_button = tk.Button(self, text="View More Posts", command=self.load_more_posts)
            view_more_button.pack(pady=10)

    def load_more_posts(self):
        self.displayed_posts = 0  # Reset the displayed count
        self.current_friend_idx = 0  # Reset to the first friend
        self.load_posts()  # Reload posts


# Function to scroll with the mouse wheel
def on_mouse_wheel(event):
    app.canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create the application instance
app = HomePageApp()

# Bind mouse scroll to the canvas
app.bind_all("<MouseWheel>", on_mouse_wheel)

# Start the application
app.mainloop()
