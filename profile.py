import re
import os
import json
import math
import subprocess
import tkinter as tk
from tkinter import font as tkFont , ttk
from tkinter import messagebox, Scrollbar ,filedialog
from PIL import Image, ImageTk

# Read file, load data
if os.path.exists("users.json"):
    with open("users.json", 'r') as file:
        users = json.load(file)
else:
    print("User data file not found. Creating a new file...")
    users = []
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

if os.path.exists("friends.json"):
    with open("friends.json", 'r') as file:
        friends_data = json.load(file)
else:
    print("Friends data file not found.")
    friends_data = {}


icon_references = []

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
max_width = min(1366, screen_width)
max_height = min(768, screen_height)
width, height = max_width, max_height
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack(fill="both", expand=True)



def create_rounded_button_icon(canvas, x, y, width, height, icon=None, command=None, radius=25):
    button_id = canvas.create_polygon(
        x + radius, y,
        x + width - radius, y,
        x + width, y + radius,
        x + width, y + height - radius,
        x + width - radius, y + height,
        x + radius, y + height,
        x, y + height - radius,
        x, y + radius,
        fill="", outline="", tags="button"
    )

    if icon:
        icon_image = Image.open(icon)
        icon_image = icon_image.resize((width, height), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_references.append(icon_photo)
        icon_id = canvas.create_image(x + width // 2, y + height // 2, image=icon_photo, tags="button")

    def on_click(event):
        if command:
            command()

    canvas.tag_bind(button_id, "<Button-1>", on_click)
    if icon:
        canvas.tag_bind(icon_id, "<Button-1>", on_click)


def create_custom_textbox(parent, x, y, width=30, height=3, font_size=14, background="#ffffff",
                          placeholder="Enter your text here...", is_password=False):
    if is_password == True:
        entry = tk.Entry(parent, width=width, font=('Arial', font_size), bd=0, highlightthickness=0,
                         background=background, show='*')
    else:

        entry = tk.Text(parent, width=width, height=height, font=('Arial', font_size), bd=0, highlightthickness=0,
                        background=background)
    entry.place(x=x, y=y)
    entry.insert('1.0' if not is_password else 0, placeholder)

    def on_click(event):
        if (entry.get('1.0', tk.END).strip() == placeholder) if not is_password else (
                entry.get() == placeholder):
            entry.delete('1.0' if not is_password else 0, tk.END)
            entry.config(fg='black')

    def on_focusout(event):
        if (entry.get('1.0', tk.END).strip() == "") if not is_password else (
                entry.get() == ""):
            entry.insert('1.0' if not is_password else 0, placeholder)
            entry.config(fg='white')

    entry.config(fg='white')

    entry.bind("<FocusIn>", on_click)
    entry.bind("<FocusOut>", on_focusout)

    return entry


def create_rounded_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)


def create_rounded_button(parent, x, y, width, height, text, command=None, radius=20,bg_color="#000000",
                          text_color="#ffffff"):
    # Create a Canvas inside the parent
    canvas = tk.Canvas(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
    canvas.place(x=x, y=y)
    canvas.config(cursor="hand2")
    button_bg = []

    button_bg.append(
        canvas.create_arc(0, 0, radius * 2, radius * 2, start=90, extent=90, fill=bg_color, outline="")
    )

    button_bg.append(
        canvas.create_arc(width - radius * 2, 0, width, radius * 2, start=0, extent=90, fill=bg_color, outline="")
    )

    button_bg.append(
        canvas.create_arc(width - radius * 2, height - radius * 2, width, height, start=270, extent=90, fill=bg_color, outline="")
    )

    button_bg.append(
        canvas.create_arc(0, height - radius * 2, radius * 2, height, start=180, extent=90, fill=bg_color, outline="")
    )

    button_bg.append(canvas.create_rectangle(radius, 0, width - radius, height, fill=bg_color, outline=""))  # Center rectangle
    button_bg.append(canvas.create_rectangle(0, radius, width, height - radius, fill=bg_color, outline=""))  # Center vertical rectangle

    button_text = canvas.create_text(width / 2, height / 2, text=text, fill=text_color, font=('Arial', 12, 'bold'))

    def on_click(event):
        if command:
            command()

    for item in button_bg:
        canvas.tag_bind(item, '<Button-1>', on_click)

    canvas.tag_bind(button_text, '<Button-1>', on_click)

    return button_bg, button_text


# Function to create gradient
def create_gradient(canvas, width, height, start_color, end_color):
    start_r = int(start_color[1:3], 16)
    start_g = int(start_color[3:5], 16)
    start_b = int(start_color[5:7], 16)

    end_r = int(end_color[1:3], 16)
    end_g = int(end_color[3:5], 16)
    end_b = int(end_color[5:7], 16)
    steps = width + height

    for i in range(steps):
        r = int(start_r + (end_r - start_r) * i / steps)
        g = int(start_g + (end_g - start_g) * i / steps)
        b = int(start_b + (end_b - start_b) * i / steps)
        color = f'#{r:02x}{g:02x}{b:02x}'

        if i < width:
            x_start = i
            y_start = 0
        else:
            x_start = width
            y_start = i - width

        if i < height:
            x_end = 0
            y_end = i
        else:
            x_end = i - height
            y_end = height

        canvas.create_line(x_start, y_start, x_end, y_end, fill=color)


# User profile page class
class UserProfilePage:
    def __init__(self, canvas, user_data):
        self.canvas = canvas
        self.user_data = user_data
        self.create_widgets()

    def create_widgets(self):
        # Create navigation bar
        self.nav_bar = tk.Frame(self.canvas, bg='gray', height=50)
        self.nav_bar_id = self.canvas.create_window(0, 0, anchor='nw', width=width, height=50, window=self.nav_bar)

        self.cover_frame = tk.Frame(self.canvas, bg='#ffffff',bd=0)
        self.cover_frame_id = self.canvas.create_window(width // 2 - 400, 50, anchor='nw', window=self.cover_frame)
        # Create cover photo
        self.cover_image = Image.open(user["cover_image"])
        self.cover_image = self.cover_image.resize((800, 200), Image.LANCZOS)
        self.cover_image = ImageTk.PhotoImage(self.cover_image)

        self.cover_photo = tk.Label(self.cover_frame, image=self.cover_image)
        self.cover_photo.image = self.cover_image
        self.cover_photo.pack(padx=0,pady=0)

        # Adjust the left frame width and height
        self.left_frame = tk.Frame(self.canvas, bg='white')
        self.left_frame_id = self.canvas.create_window(10, 150, anchor='nw', window=self.left_frame)

        # Create profile image inside the left frame
        self.profile_image = Image.open(user["profile_image"])
        self.profile_image = self.profile_image.resize((100, 100), Image.LANCZOS)
        self.profile_image = ImageTk.PhotoImage(self.profile_image)

        self.profile_image_label = tk.Label(self.left_frame, image=self.profile_image)
        self.profile_image_label.image = self.profile_image
        self.profile_image_label.pack(pady=5)  # Add some space around the profile image

        # Create labels and entries for user details inside the left frame
        self.username_label = tk.Label(self.left_frame, text=f"{user['username']}", font=("Arial",16),anchor="center")
        self.username_label.pack(pady=1)

        self.email_label = tk.Label(self.left_frame, text=f"Email: {user['Email']}")
        self.email_label.pack(pady=5)

        self.phone_number_label = tk.Label(self.left_frame, text=f"Phone Number: {user['Phone Number']}")
        self.phone_number_label.pack(pady=5)

        self.gender_label = tk.Label(self.left_frame, text=f"Gender: {user['Gender']}")
        self.gender_label.pack(pady=5)

        self.governorate_label = tk.Label(self.left_frame, text=f"Governorate: {user['Governorate']}")
        self.governorate_label.pack(pady=5)

        self.age_label = tk.Label(self.left_frame, text=f"Age: {user['Age']}")
        self.age_label.pack(pady=5)

        self.mid_frame=self.create_scrollable_frame(x=width // 2 - 300, y=280, width=600, height=400, bg='white', title='Posts')
        self.create_friends_frame()


    def create_friends_frame(self):

        self.right_frame = self.create_scrollable_friends_frame(x=width - 270, y=180, width=240, height=400, bg='white')

        user_friends = friends_data.get(user["Email"], {})

        # Display friends in the scrollable frame
        for friend_name, friend_email in user_friends.items():
            self.add_friend_to_frame(self.right_frame, friend_name, friend_email)

    def create_scrollable_friends_frame(self, x, y, width, height, bg):

        scroll_canvas = tk.Canvas(self.canvas, bg=bg, width=width, height=height)
        scroll_canvas_id = self.canvas.create_window(x, y, anchor='nw', window=scroll_canvas)


        scrollbar = tk.Scrollbar(self.canvas, orient='vertical', command=scroll_canvas.yview)
        scrollbar_id = self.canvas.create_window(x + width - 10, y, height=height, anchor='ne', window=scrollbar)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)


        inner_frame = tk.Frame(scroll_canvas, bg=bg)
        inner_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))


        scroll_canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        return inner_frame

    def add_friend_to_frame(self, parent, friend_name, friend_email):

        friend_frame = tk.Frame(parent, bg='lightgray', padx=5, pady=5)
        friend_frame.pack(fill='x', pady=5)


        friend_label = tk.Label(friend_frame, text=friend_name, font=("Arial", 12), anchor="w", bg='lightgray',
                                cursor="hand2")
        friend_label.pack(side="left", padx=10)


        def open_friend_profile(event):
            # Find friend's data from users list
            for f_img in users:
                if f_img["Email"] == friend_email:
                    friend_data = f_img
                    break
            else:
                friend_data = None


            if friend_data:
                read_only_profile_page = ReadOnlyProfilePage(self.canvas, friend_data)


        friend_label.bind("<Button-1>", open_friend_profile)


        for f_img in users:
            if f_img["Email"] == friend_email:
                friend_p_img = f_img["profile_image"]
                placeholder_image = Image.open(friend_p_img)
                placeholder_img = placeholder_image.resize((40, 40), Image.LANCZOS)
                placeholder_photo = ImageTk.PhotoImage(placeholder_img)

                profile_image_label = tk.Label(friend_frame, image=placeholder_photo, cursor="hand2")
                profile_image_label.image = placeholder_photo
                profile_image_label.pack(side="right", padx=10)
                break
        else:
            placeholder_image = Image.new("RGB", (40, 40), color="gray")
            placeholder_photo = ImageTk.PhotoImage(placeholder_image)

            profile_image_label = tk.Label(friend_frame, image=placeholder_photo)
            profile_image_label.image = placeholder_photo
            profile_image_label.pack(side="right", padx=10)
    def create_scrollable_frame(self, x, y, width, height, bg, title):
        # Create a canvas to hold the scrolling frame
        scroll_canvas = tk.Canvas(self.canvas, bg=bg, width=width, height=height)
        scroll_canvas_id = self.canvas.create_window(x, y, anchor='nw', window=scroll_canvas)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.canvas, orient='vertical', command=scroll_canvas.yview)
        scrollbar_id = self.canvas.create_window(x + width - 10, y, height=height, anchor='ne', window=scrollbar)

        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        # Create an inner frame inside the canvas
        inner_frame = tk.Frame(scroll_canvas, bg=bg)

        # Bind the frame size to the canvas scroll region
        inner_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

        # Place the inner frame inside the canvas
        scroll_canvas.create_window((0, 0), window=inner_frame, anchor='nw')

def login_page():
        root.destroy()
        subprocess.run(["python", "login.py"])
        user["login_status"] = "false"
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

# User page class
class UserPage(UserProfilePage):
    def __init__(self, canvas, user_data):
        super().__init__(canvas, user_data)
        if isinstance(self, UserProfilePage) and not isinstance(self, ReadOnlyProfilePage):
            self.create_editing_methods()

    def create_editing_methods(self):
        def edit_info():
            new_window = tk.Toplevel(self.canvas)
            new_window.title("Edit Info")
            new_window.geometry("500x500")
            create_gradient(canvas, width, height, start_color, end_color)

            y_offset = 20  # Starting y-offset for the labels and entries
            fields = ["bio", "username", "Email", "Phone Number", "Governorate", "Age"]
            entries = []

            for i, field in enumerate(fields):
                label = ttk.Label(new_window, text=field)
                entry = ttk.Entry(new_window, width=30)
                label.pack(pady=5)
                entry.pack(pady=5)
                entries.append(entry)

                # Pre-fill the entries with current user data
                entry.insert(0, user[field])  # Assuming user has attributes that match these fields

            def save_update():
                # Save the updates back to the user data
                user['bio'] = entries[0].get()
                user['username'] = entries[1].get()
                user['Email'] = entries[2].get()
                user['Phone Numberr'] = entries[3].get()
                user['Governorate'] = entries[4].get()
                user['Age'] = entries[5].get()

                # Optionally, save the updated user data back to the JSON file
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)

                new_window.destroy()  # Close the window after saving

            # Create a save button
            save_button = tk.Button(new_window, text="Save", command=save_update, anchor="center")
            save_button.pack(pady=20)

        def edit_cover_image():
            file_path = filedialog.askopenfilename(
                title="Select Cover Image",
                filetypes=(("Image Files", "*.jpg;*.jpeg;*.png;*.gif"), ("All Files", "*.*"))
            )
            if file_path:
                # Update cover image in user data
                user['cover_image'] = file_path
                # Optionally, update the displayed cover image
                self.cover_image = Image.open(file_path)
                self.cover_image = self.cover_image.resize((800, 200), Image.LANCZOS)
                self.cover_image = ImageTk.PhotoImage(self.cover_image)
                self.cover_photo.configure(image=self.cover_image)
                self.cover_photo.image = self.cover_image

                # Save updated user data to JSON
                with open("users.json", 'w') as file:
                    json.dump(users, file, indent=4)

        def edit_profile_image():
            file_path = filedialog.askopenfilename(
                title="Select Profile Image",
                filetypes=(("Image Files", "*.jpg;*.jpeg;*.png;*.gif"), ("All Files", "*.*"))
            )
            if file_path:
                # Update profile image in user data
                user['profile_image'] = file_path
                # Optionally, update the displayed profile image
                self.profile_image = Image.open(file_path)
                self.profile_image = self.profile_image.resize((100, 100), Image.LANCZOS)
                self.profile_image = ImageTk.PhotoImage(self.profile_image)
                self.profile_image_label.configure(image=self.profile_image)
                self.profile_image_label.image = self.profile_image

                # Save updated user data to JSON
                with open("users.json", 'w') as file:
                    json.dump(users, file, indent=4)

        def post():
            return

        self.edit_profile_button = tk.Button(self.left_frame, text='Edit info',command=edit_info)
        self.edit_profile_button.pack(fill='x', pady=5)

        self.edit_cover_button = tk.Button(self.left_frame, text='Edit Cover Photo',command=edit_cover_image)
        self.edit_cover_button.pack(fill='x', pady=5)

        self.edit_profile_image_button = tk.Button(self.left_frame, text='Edit Profile Image',command=edit_profile_image)
        self.edit_profile_image_button.pack(fill='x', pady=5)
        self.edit_profile_image_button = tk.Button(self.left_frame, text='Log Out',
                                                   command=login_page)
        self.edit_profile_image_button.pack(fill='x', pady=5)

        post = create_rounded_button(self.mid_frame,560,290,250,25,text="Whats in your mind?",
                                     command=post,radius=60,bg_color="#76b5c5",text_color="#000000")


class ReadOnlyProfilePage(UserProfilePage):
    def __init__(self, canvas, friend_data):
        self.canvas = canvas
        self.friend_data = friend_data
        self.create_widgets()

    def create_widgets(self):
        # Create navigation bar
        self.nav_bar = tk.Frame(self.canvas, bg='gray', height=50)
        self.nav_bar_id = self.canvas.create_window(0, 0, anchor='nw', width=width, height=50, window=self.nav_bar)

        # Create cover photo
        self.cover_frame = tk.Frame(self.canvas, bg='#ffffff', bd=0)
        self.cover_frame_id = self.canvas.create_window(width // 2 - 400, 50, anchor='nw', window=self.cover_frame)

        self.cover_image = Image.open(self.friend_data["cover_image"])
        self.cover_image = self.cover_image.resize((800, 200), Image.LANCZOS)
        self.cover_image = ImageTk.PhotoImage(self.cover_image)

        self.cover_photo = tk.Label(self.cover_frame, image=self.cover_image)
        self.cover_photo.image = self.cover_image
        self.cover_photo.pack(padx=0, pady=0)

        # Left frame for friend details
        self.left_frame = tk.Frame(self.canvas, bg='white')
        self.left_frame_id = self.canvas.create_window(10, 150, anchor='nw', window=self.left_frame)

        # Profile image inside the left frame
        self.profile_image = Image.open(self.friend_data["profile_image"])
        self.profile_image = self.profile_image.resize((100, 100), Image.LANCZOS)
        self.profile_image = ImageTk.PhotoImage(self.profile_image)

        self.profile_image_label = tk.Label(self.left_frame, image=self.profile_image)
        self.profile_image_label.image = self.profile_image
        self.profile_image_label.pack(pady=5)

        # Create labels for friend details inside the left frame
        self.username_label = tk.Label(self.left_frame, text=f"{self.friend_data['username']}", font=("Arial", 16), anchor="center")
        self.username_label.pack(pady=1)

        self.email_label = tk.Label(self.left_frame, text=f"Email: {self.friend_data['Email']}")
        self.email_label.pack(pady=5)

        self.phone_number_label = tk.Label(self.left_frame, text=f"Phone Number: {self.friend_data['Phone Number']}")
        self.phone_number_label.pack(pady=5)

        self.gender_label = tk.Label(self.left_frame, text=f"Gender: {self.friend_data['Gender']}")
        self.gender_label.pack(pady=5)

        self.governorate_label = tk.Label(self.left_frame, text=f"Governorate: {self.friend_data['Governorate']}")
        self.governorate_label.pack(pady=5)

        self.age_label = tk.Label(self.left_frame, text=f"Age: {self.friend_data['Age']}")
        self.age_label.pack(pady=5)

        self.mid_frame = self.create_scrollable_frame(x=width // 2 - 300, y=280, width=600, height=400, bg='white', title='Friends')
        self.create_friends_frame()



def load_user_data(username):
    with open("users.json", "r") as f:
        users = json.load(f)
        for user in users:
            if user["username"] == username:
                return user
    return None


current_user = None
logged_in = False

for user in users:
    if user["login_status"] == "true":
        current_user = user["username"]
        logged_in = True
        break

if not logged_in:
    message = f"no logged user!"
    messagebox.showerror("Error", message)
    login_page()


user_data = load_user_data(current_user)

if user_data:
    root.title("Profile Page")

    # Draw gradient background
    start_color = "#74889d"
    end_color = "#26609a"
    create_gradient(canvas, width, height, start_color, end_color)

    # Set window size
    root.geometry(f"{max_width}x{max_height}")

    # Create the user profile page on the canvas
    profile_page = UserPage(canvas, user_data)

    root.mainloop()
else:
    print("User not found!")
