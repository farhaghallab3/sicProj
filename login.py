import re
import os
import json
import math
import random
import subprocess
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk

# Read file, load data
if os.path.exists("users.json"):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except json.JSONDecodeError:
        print("Error parsing JSON file. Please check the file format.")
        users = []
else:
    print("User data file not found. Creating a new file...")
    users = []
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

icon_references = []


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


def create_rounded_button(canvas, x, y, width, height, text, command=None, radius=20, bg_color="#4CAF50",
                          text_color="#ffffff"):
    button_bg = []

    button_bg.append(
        canvas.create_arc(x, y, x + radius * 2, y + radius * 2, start=90, extent=90, fill=bg_color, outline=""))

    button_bg.append(
        canvas.create_arc(x + width - radius * 2, y, x + width, y + radius * 2, start=0, extent=90, fill=bg_color,
                          outline=""))

    button_bg.append(
        canvas.create_arc(x + width - radius * 2, y + height - radius * 2, x + width, y + height, start=270, extent=90,
                          fill=bg_color, outline=""))

    button_bg.append(
        canvas.create_arc(x, y + height - radius * 2, x + radius * 2, y + height, start=180, extent=90, fill=bg_color,
                          outline=""))

    button_bg.append(canvas.create_rectangle(x + radius, y, x + width - radius, y + height, fill=bg_color,
                                             outline=""))  # Center rectangle
    button_bg.append(canvas.create_rectangle(x, y + radius, x + width, y + height - radius, fill=bg_color,
                                             outline=""))  # Center vertical rectangle

    button_text = canvas.create_text(x + width / 2, y + height / 2, text=text, fill=text_color,
                                     font=('Arial', 12, 'bold'))

    def on_click(event):
        if command:
            command()

    for item in button_bg:
        canvas.tag_bind(item, '<Button-1>', on_click)

    canvas.tag_bind(button_text, '<Button-1>', on_click)

    return button_bg, button_text

def open_register():
    root.destroy()
    subprocess.run(["python", "register.py"])

def open_profile():
    root.destroy()
    subprocess.run(["python", "profile.py"])

def login_page():

    exit_button()

    def validate_login(email_entry, password_entry, users):
        email = email_entry.get("1.0", tk.END).strip() if isinstance(email_entry, tk.Text) else email_entry.get()
        password = password_entry.get()
        global user
        for user in users:
            if user["Email"] == email and user["Password"] == password:
                global current_user
                current_user = user["username"]
                message = f"Login successful, welcome {current_user}!"
                messagebox.showinfo("Login Successful", message)
                user["login_status"] = "true"

                with open("users.json", "w") as file:
                    json.dump(users, file, indent=4)
                open_profile()
                return

        messagebox.showerror("Login Failed", "Invalid username or password")



    form_width = width * 0.4
    form_height = height * 0.5
    form_x1 = (width - form_width) // 2
    form_y1 = (height - form_height) // 2
    form_x2 = form_x1 + form_width
    form_y2 = form_y1 + form_height

    create_rounded_rectangle(form_x1, form_y1, form_x2, form_y2, radius=60, fill="white")

    create_rounded_button_icon(canvas, form_x1 + 215, form_y1 - 80, 120, 120,
                               icon="F:/moh/python-projects/sicProj/assets/user.png", radius=40)

    entry_height = 50
    create_rounded_rectangle(form_x1 + 20, form_y1 + 85, form_x2 - 20, form_y1 + 90 + entry_height, radius=60,
                             fill="#5A6B6F")
    canvas.create_oval(width // 3 - 40, form_y1 + 70, width // 3 + 40, form_y1 + 150, fill="#ffffff", outline="")
    create_rounded_button_icon(canvas, form_x1, form_y1 + 63, 95, 95,
                               icon="F:/moh/python-projects/sicProj/assets/email.png", radius=40)

    email_entry = create_custom_textbox(canvas, form_x1 + 90, form_y1 + 98, 38, 1.3, background="#5A6B6F")

    create_rounded_rectangle(form_x1 + 20, form_y1 + 180, form_x2 - 20, form_y1 + 180 + entry_height, radius=60,
                             fill="#5A6B6F")
    canvas.create_oval(width // 3 - 40, form_y1 + 160, width // 3 + 40, form_y1 + 240, fill="#ffffff", outline="")
    create_rounded_button_icon(canvas, form_x1, form_y1 + 153, 95, 95,
                               icon="F:/moh/python-projects/sicProj/assets/password.png", radius=40)

    password_entry = create_custom_textbox(canvas, form_x1 + 90, form_y1 + 193, 38, 1.3, background="#5A6B6F",
                                           is_password=True)

    remember_var = tk.BooleanVar()

    remember_me_checkbox = tk.Checkbutton(canvas, text="Remember Me", font=('Arial', 12), variable=remember_var)
    remember_me_checkbox.place(x=470, y=435)

    create_rounded_button(canvas, form_x1 + 50, form_y2 - 100, 450, 50, "login",
                          command=lambda: validate_login(email_entry, password_entry,users), bg_color="#5A6B6F")

    not_user_label = tk.Label(canvas, text="Don't have an account? ", fg="#000000", font=("Arial", 16))
    not_user_label.place(relx=0.365, rely=0.721)
    register_label = tk.Label(canvas, text="Register", fg="blue", font=("Arial", 19), cursor="hand2")
    register_label.place(x=730, y=537)
    register_label.bind("<Button-1>", lambda e: open_register())


def exit_button():
    icon_path = "F:/moh/python-projects/SIC_Shop/Ch6_project/logout.png"
    try:
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((70, 70), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        canvas.image = icon_photo
        create_rounded_button_icon(canvas, width - 150, height - 200, 70, 70, icon=icon_path, command=root.quit,
                                   radius=40)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load icon: {e}")


root = tk.Tk()
root.title("Registration Page")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

max_width = min(1366, screen_width)
max_height = min(768, screen_height)

root.geometry(f"{max_width}x{max_height}")

width, height = max_width, max_height
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

start_color = "#74889d"
end_color = "#26609a"
create_gradient(canvas, width, height, start_color, end_color)

title_font = tkFont.Font(family="Arial", size=24, weight="bold")
label_font = tkFont.Font(family="Arial", size=12)
button_font = tkFont.Font(family="Arial", size=14, weight="bold")

login_page()

root.mainloop()