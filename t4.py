import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Page Navigation")

        # Create frames for different pages
        self.frame1 = Frame1(self)
        self.frame2 = Frame2(self)

        # Show the first frame
        self.frame1.pack(fill="both", expand=True)

    def show_frame(self, frame):
        """Hide the current frame and show the specified frame."""
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        frame.pack(fill="both", expand=True)

class Frame1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="This is Frame 1")
        label.pack(pady=20)
        button = tk.Button(self, text="Go to Frame 2", command=lambda: parent.show_frame(parent.frame2))
        button.pack(pady=10)

class Frame2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="This is Frame 2")
        label.pack(pady=20)
        button = tk.Button(self, text="Go to Frame 1", command=lambda: parent.show_frame(parent.frame1))
        button.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
