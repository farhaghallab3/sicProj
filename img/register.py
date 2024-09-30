import re
import os
import json
import math
import subprocess
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

import users
from PIL import Image, ImageTk

# Read file, load data
if os.path.exists("users.json"):
    with open("users.json", 'r') as users_file:
        users_list = json.load(users_file)

else:
    print("User data file not found. Creating a new file...")
    users_list = []
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

icon_references=[]
def create_rounded_button_icon( canvas, x, y, width, height, icon=None, command=None, radius=25):
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

def create_gradient(canvas, width, height, start_color, end_color):
    start_r = int(start_color[1:3], 16)
    start_g = int(start_color[3:5], 16)
    start_b = int(start_color[5:7], 16)

    end_r = int(end_color[1:3], 16)
    end_g = int(end_color[3:5], 16)
    end_b = int(end_color[5:7], 16)
    diagonal_length = int(math.sqrt(width ** 2 + height ** 2))

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


def create_rounded_button(canvas, x, y, width, height, text=None, icon=None, command=None, radius=25, bg="#CFB095",
                          active_bg="#FFE4C4", text_color='#ffffff', cursor="hand2"):
    # Create the rounded rectangle by drawing 4 arcs and 4 rectangles
    points = [x + radius, y, x + width - radius, y, x + width, y, x + width, y + radius, x + width,
              y + height - radius, x + width, y + height, x + width - radius, y + height,
              x + radius, y + height, x, y + height, x, y + height - radius, x, y + radius, x, y]

    button_shape = canvas.create_polygon(points, smooth=True, fill=bg, outline="", tags="button_shape")

    # Add text on top of the rounded rectangle
    if text:
        text_label = canvas.create_text(x + width / 2, y + height / 2, text=text, fill=text_color,
                                        font=("Arial", 12, "bold"), tags="button_text")

    # Add icon if provided
    if icon:
        image = Image.open(icon)
        image = image.resize((int(height * 0.6), int(height * 0.6)), Image.ANTIALIAS)  # Resize icon to fit the button
        icon_image = ImageTk.PhotoImage(image)
        canvas.create_image(x + width / 2, y + height / 2, image=icon_image, tags="button_icon")
        canvas.image = icon_image  # Prevent image from being garbage collected

    # Define hover effects and click behavior
    def on_enter(event):
        canvas.itemconfig(button_shape, fill=active_bg)

    def on_leave(event):
        canvas.itemconfig(button_shape, fill=bg)

    def on_click(event):
        if command:
            command()

    # Bind events to the canvas object
    canvas.tag_bind("button_shape", "<Enter>", on_enter)
    canvas.tag_bind("button_shape", "<Leave>", on_leave)
    canvas.tag_bind("button_shape", "<Button-1>", on_click)

    if text:
        text_label = canvas.create_text(x + width / 2, y + height / 2, text=text, fill=text_color,
                                        font=("Arial", 12, "bold"), tags=("button", "button_text"))

        # Add icon if provided
    if icon:
        image = Image.open(icon)
        image = image.resize((int(height * 0.6), int(height * 0.6)), Image.ANTIALIAS)  # Resize icon to fit the button
        icon_image = ImageTk.PhotoImage(image)
        canvas.create_image(x + width / 2, y + height / 2, image=icon_image, tags=("button", "button_icon"))
        canvas.image = icon_image  # Prevent image from being garbage collected

        # Define hover effects and click behavior

    def on_enter(event):
        canvas.itemconfig(button_shape, fill=active_bg)
        canvas.config(cursor=cursor)

    def on_leave(event):
        canvas.itemconfig(button_shape, fill=bg)
        canvas.config(cursor="")

    def on_click(event):
        if command:
            command()

        # Bind hover and click events for all parts of the button (shape, text, and icon)

    for tag in ("button_shape", "button_text", "button_icon"):
        canvas.tag_bind(tag, "<Enter>", on_enter)
        canvas.tag_bind(tag, "<Leave>", on_leave)
        canvas.tag_bind(tag, "<Button-1>", on_click)

def register_page():

    def validate_data():
        errors = []
        if not name_var.get().strip():
            errors.append("- Name cannot be empty.")
        if not re.match(r'^\d{10,15}$', phone_var.get()):
            errors.append("- Phone number must be 10-15 digits long.")
        if not re.match(r'^\S+@\S+\.\S+$', email_var.get()):
            errors.append("- Invalid email format.")
        if not gender_var.get().strip():
            errors.append("- Gender cannot be empty.")
        if not governorate_var.get().strip():
            errors.append("- Governorate cannot be empty.")
        if len(password_var.get()) < 6:
            errors.append("- Password must be at least 6 characters long.")
        try:
            age = int(age_var.get())
            if age <= 0:
                errors.append("- Age must be a positive number.")
        except ValueError:
            errors.append("- Age must be a valid integer.")
        if re_password_var.get() != password_var.get():
            errors.append("- password not match.")

        return errors

    def register_user():
        errors = validate_data()
        if errors:
            error_message = "\n".join(errors)
            messagebox.showerror("Invalid Input", error_message)
            return
        user_id = len(users_list) + 1
        user_data = {
            "ID": user_id,
            "username": name_var.get(),
            "Phone Number": phone_var.get(),
            "Email": email_var.get(),
            "Gender": gender_var.get(),
            "Governorate": governorate_var.get(),
            "Password": password_var.get(),
            "Age": age_var.get(),
            "login_status": False,
            "friends_counter":0,
            "friends":[],
            "profile_image":"",
            "cover_image":"",
            "bio":""
        }

        if not os.path.exists("users.json"):
            with open("users.json", "w") as file:
                json.dump([], file, indent=4)

        with open("users.json", "r+") as file:
            users = json.load(file)
            users.append(user_data)
            file.seek(0)
            json.dump(users, file, indent=4)

        messagebox.showinfo("Success", "Registration successful!")

    frame_width = 800
    frame_height = 400
    x1 = (width - frame_width) // 2
    y1 = (height - frame_height) // 2
    x2 = x1 + frame_width
    y2 = y1 + frame_height
    create_rounded_rectangle(x1, y1, x2, y2, radius=40, fill="#ffffff", outline="")



    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    gender_var = tk.StringVar()
    governorate_var = tk.StringVar()
    password_var = tk.StringVar()
    re_password_var = tk.StringVar()
    age_var = tk.StringVar()

    register_label = tk.Label(canvas, text="Register", font=title_font, bg="#ffffff", fg="black")
    register_label.place(x=x1 + frame_width // 2, y=y1 + 24, anchor="center")

    # Left column labels and entries
    name_label = tk.Label(canvas, text="Name", font=label_font, bg="#ffffff")
    name_label.place(x=x1 + 70, y=y1 + 80)
    name_entry = tk.Entry(canvas, font=label_font, textvariable=name_var, width=30)
    name_entry.place(x=x1 + 70, y=y1 + 110)

    phone_label = tk.Label(canvas, text="Phone Number", font=label_font, bg="#ffffff")
    phone_label.place(x=x1 + 70, y=y1 + 150)
    phone_entry = tk.Entry(canvas, font=label_font, textvariable=phone_var, width=30)
    phone_entry.place(x=x1 + 70, y=y1 + 180)

    email_label = tk.Label(canvas, text="Email", font=label_font, bg="#ffffff")
    email_label.place(x=x1 + 70, y=y1 + 220)
    email_entry = tk.Entry(canvas, font=label_font, textvariable=email_var, width=30)
    email_entry.place(x=x1 + 70, y=y1 + 250)

    gender_label = tk.Label(canvas, text="Gender", font=label_font, bg="#ffffff")
    gender_label.place(x=x1 + 70, y=y1 + 290)
    gender_entry = tk.Entry(canvas, font=label_font, textvariable=gender_var, width=10)
    gender_entry.place(x=x1 + 70, y=y1 + 320)

    # Right column labels and entries
    governorate_label = tk.Label(canvas, text="Governorate", font=label_font, bg="#ffffff")
    governorate_label.place(x=x1 + 460, y=y1 + 80)
    governorate_entry = tk.Entry(canvas, font=label_font, textvariable=governorate_var, width=20)
    governorate_entry.place(x=x1 + 460, y=y1 + 110)

    password_label = tk.Label(canvas, text="Password", font=label_font, bg="#ffffff")
    password_label.place(x=x1 + 460, y=y1 + 150)
    password_entry = tk.Entry(canvas, font=label_font, textvariable=password_var, width=20, show="*")
    password_entry.place(x=x1 + 460, y=y1 + 180)

    re_password_label = tk.Label(canvas, text="re-enter password", font=label_font, bg="#ffffff")
    re_password_label.place(x=x1 + 460, y=y1 + 220)
    re_password_entry = tk.Entry(canvas, font=label_font, textvariable=re_password_var, width=30, show="*")
    re_password_entry.place(x=x1 + 460, y=y1 + 250)

    age_label = tk.Label(canvas, text="Age", font=label_font, bg="#ffffff")
    age_label.place(x=x1 + 460, y=y1 + 290)
    age_entry = tk.Entry(canvas, font=label_font, textvariable=age_var, width=10)
    age_entry.place(x=x1 + 460, y=y1 + 320)


    register_button = create_rounded_button(canvas,x1 + frame_width -190,y1 + 340,width=180 ,height=45, text="Register",command=register_user,radius=30, bg="#26609a", active_bg="white")


    login_button = create_rounded_button(canvas,x1 + frame_width +50,y1 + 450,width=180 ,height=45, text="Go to Login",radius=30, bg="#ffffff", active_bg="white",
                              text_color="#000000",command=login_page)






def login_page():
    root.destroy()
    subprocess.run(["python", "login.py"])
root = tk.Tk()
root.title("Registration Page")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

max_width = min(1366, screen_width)
max_height = min(768, screen_height)

root.geometry(f"{max_width}x{max_height}")



width, height =max_width , max_height
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

start_color = "#74889d"
end_color = "#26609a"
create_gradient(canvas, width, height, start_color, end_color)

title_font = tkFont.Font(family="Arial", size=24, weight="bold")
label_font = tkFont.Font(family="Arial", size=12)
button_font = tkFont.Font(family="Arial", size=14, weight="bold")

register_page()

root.mainloop()