import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from FriendRequestsLogic import UserData, IncomingRequestsLogic, OutgoingRequestsLogic
##
# Function to load and resize an image
def load_image(image_path, size=(60, 60)):
    try:
        img = Image.open(image_path).resize(size, Image.LANCZOS)  # Use LANCZOS for quality
        return img
    except Exception as e:
        print("Error loading image:", e)
        return None

# Initialize incoming requests logic
inc_obj = IncomingRequestsLogic("ahmed.ibrahim@gmail.com")
inc_data = inc_obj.collect_incoming_requests_data()

outg_obj = OutgoingRequestsLogic("ahmed.ibrahim@gmail.com")
outg_data = outg_obj.collect_outgoing_requests_data()

# Create the main window
class FriendRequestsApp(tk.Tk):
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

        # Initialize the frames for friend requests
        self.incoming_requests = IncomingRequests(self.scrollable_frame, self)
        self.outgoing_requests = OutgoingRequests(self.scrollable_frame, self)

        # Show the incoming requests frame by default
        self.show_frame(self.incoming_requests)

        # Create navigation buttons
        self.nav_button_incoming = tk.Button(self, text="Incoming Requests", command=lambda: self.show_frame(self.incoming_requests))
        self.nav_button_outgoing = tk.Button(self, text="Outgoing Requests", command=lambda: self.show_frame(self.outgoing_requests))

        # Place navigation buttons
        self.nav_button_incoming.place(x=10, y=top_distance + 10)  # Adjust x and y for margins
        self.nav_button_outgoing.place(x=10, y=top_distance + 50)  # Below the first button

    def show_frame(self, frame):
        """Hide the current frame and show the specified frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()  # Clear current contents
        frame.pack(fill="both", expand=True)  # Pack the new frame


class IncomingRequests(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.buttons = {}  # Dictionary to store button references

        for request in inc_data:
            sender_name = request["name"]
            profile_photo = request["profile photo"]
            fr_mail = request["fr mail"]
            random_param = request.get("random parameter", "No parameter")  # Fetch random parameter

            # Create a frame for each friend request with a specified width
            request_frame = tk.Frame(self, bd=2, relief=tk.RAISED, padx=10, pady=10, width=300)  # Set desired width
            request_frame.pack(fill="x", pady=5, padx=20)  # Add horizontal padding

            # Load and display the profile photo
            img = load_image(profile_photo)
            if img:
                img_tk = ImageTk.PhotoImage(img)
                photo_label = tk.Label(request_frame, image=img_tk)
                photo_label.image = img_tk  # Keep a reference
                photo_label.grid(row=0, column=0, padx=5, pady=5)

            # Create a frame for the text details
            details_frame = tk.Frame(request_frame)
            details_frame.grid(row=0, column=1, padx=10, sticky="w")

            # Display the sender's name in bold
            name_label = tk.Label(details_frame, text=sender_name, font=("Helvetica", 12, "bold"))
            name_label.pack(anchor="w")

            # Display the random parameter
            random_param_label = tk.Label(details_frame, text=random_param, font=("Helvetica", 10))
            random_param_label.pack(anchor="w")

            # Add buttons for accept and decline
            button_frame = tk.Frame(request_frame)
            button_frame.grid(row=0, column=2, sticky="e")

            # Create Accept button
            accept_button = tk.Button(
                button_frame,
                text="Accept",
                command=lambda email=fr_mail: self.handle_request(email, "accept")
            )
            accept_button.pack(side="top", padx=5, pady=2)

            # Create Decline button
            decline_button = tk.Button(
                button_frame,
                text="Decline",
                command=lambda email=fr_mail: self.handle_request(email, "decline")
            )
            decline_button.pack(side="top", padx=5, pady=2)

    def handle_request(self, fr_mail, action):
        """Handle the friend request action (accept or decline)."""
        if action == "accept":
            print(f"Accepted friend request from {fr_mail}")
            inc_obj.accept_fr_req(fr_mail)
        elif action == "decline":
            print(f"Declined friend request from {fr_mail}")
            inc_obj.decline_fr_req(fr_mail)


class OutgoingRequests(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        for request in outg_data:
            sender_name = request["name"]
            profile_photo = request["profile photo"]
            fr_mail = request["fr mail"]
            random_param = request["random parameter"]  # New parameter
            request_status = request["request status"]  # New parameter

            # Create a frame for each outgoing request with a specified width
            request_frame = tk.Frame(self, bd=2, relief=tk.RAISED, padx=10, pady=10, width=300)
            request_frame.pack(fill="x", pady=5, padx=20)  # Add horizontal padding

            # Load and display the profile photo
            img = load_image(profile_photo)
            if img:
                img_tk = ImageTk.PhotoImage(img)
                photo_label = tk.Label(request_frame, image=img_tk)
                photo_label.image = img_tk  # Keep a reference
                photo_label.grid(row=0, column=0, padx=5, pady=5)

            # Create a frame for the text details
            details_frame = tk.Frame(request_frame)
            details_frame.grid(row=0, column=1, padx=10, sticky="w")

            # Display the sender's name in bold
            name_label = tk.Label(details_frame, text=sender_name, font=("Helvetica", 12, "bold"))
            name_label.pack(anchor="w")

            # Display the random parameter
            random_param_label = tk.Label(details_frame, text=random_param, font=("Helvetica", 10))
            random_param_label.pack(anchor="w")

            # Display the request status
            status_label = tk.Label(details_frame, text=f"Status: {request_status}", font=("Helvetica", 10))
            status_label.pack(anchor="w", pady=(5, 0))  # Add some padding for separation

            # Add an "OK" button and place it at the bottom right of the frame
            ok_button = tk.Button(request_frame, text="OK", command=lambda mail=fr_mail: self.handle_ok(mail))
            ok_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")  # Fixed position on the right side

    def handle_ok(self, fr_mail):
        """Handle the OK action for outgoing requests."""
        outg_obj.sent_ok(fr_mail)
        print(f"OK clicked for request to {fr_mail}")



# Function to scroll with the mouse wheel
def on_mouse_wheel(event):
    app.canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create the application instance
app = FriendRequestsApp()

# Bind mouse scroll to the canvas
app.bind_all("<MouseWheel>", on_mouse_wheel)

# Start the application
app.mainloop()
