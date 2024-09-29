import tkinter as tk
from tkinter import ttk

# Create the main window
class FriendRequestsApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Get screen dimensions, excluding taskbar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight() - 40  # Adjust for taskbar height (adjust as necessary)

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

        # Initialize the frames for different pages
        self.outgoing_requests = OutgoingRequests(self.scrollable_frame, self)
        self.incoming_requests = IncomingRequests(self.scrollable_frame, self)

        # Show the first frame
        self.show_frame(self.outgoing_requests)

        # Create navigation buttons
        self.nav_button_outgoing = tk.Button(self, text="Outgoing Requests", command=lambda: self.show_frame(self.outgoing_requests))
        self.nav_button_incoming = tk.Button(self, text="Incoming Requests", command=lambda: self.show_frame(self.incoming_requests))

        # Place navigation buttons
        self.nav_button_outgoing.place(x=10, y=top_distance + 10)  # Adjust x and y for margins
        self.nav_button_incoming.place(x=10, y=top_distance + 50)  # Below the first button

    def show_frame(self, frame):
        """Hide the current frame and show the specified frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()  # Clear current contents
        frame.pack(fill="both", expand=True)  # Pack the new frame

class OutgoingRequests(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        for i in range(1, 80):  # Add 5 items for testing
            item_frame = tk.Frame(self, bd=2, relief=tk.RAISED, bg="lightblue")
            item_frame.pack(fill=tk.X, pady=5, padx=10)  # Add padding for centering

            long_text = ("This is a long paragraph intended to test the wrapping behavior of the frame. " * 5)  # Long text for testing
            text_box = tk.Text(item_frame, wrap=tk.WORD, height=4, width=50)
            text_box.insert(tk.END, long_text)
            text_box.pack(padx=10, pady=5)

class IncomingRequests(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        for i in range(81, 170):  # Add 5 items for testing
            item_frame = tk.Frame(self, bd=2, relief=tk.RAISED, bg="lightblue")
            item_frame.pack(fill=tk.X, pady=5, padx=10)  # Add padding for centering

            long_text = ("This is another long paragraph intended to test the wrapping behavior of the frame. " * 5)  # Long text for testing
            text_box = tk.Text(item_frame, wrap=tk.WORD, height=4, width=50)
            text_box.insert(tk.END, long_text)
            text_box.pack(padx=10, pady=5)

# Function to scroll with the mouse wheel
def on_mouse_wheel(event):
    app.canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create the application instance
app = FriendRequestsApp()

# Bind mouse scroll to the canvas
app.bind_all("<MouseWheel>", on_mouse_wheel)

# Start the application
app.mainloop()
