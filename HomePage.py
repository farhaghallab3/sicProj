import re
import os
import json
import math
import subprocess
import tkinter as tk
from tkinter import font as tkFont , ttk
from tkinter import messagebox, Scrollbar ,filedialog
from PIL import Image, ImageTk
from datetime import datetime

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
max_width = min(1280, screen_width)
max_height = min(200, screen_height)
width, height = max_width, max_height
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack(fill="both", expand=True)
root.resizable(False, False)


class HomePage:
    def __init__(self):
        add_p_fr = tk.Frame(root, bg="gray", width=550, height=500, padx=10, pady=10)
        canvas.create_window((width//2, height//2), window=add_p_fr, anchor="center")


homeP = HomePage()
root.mainloop()