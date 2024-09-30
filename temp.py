
class View_Friends_Posts(tk.Frame):
    def __init__(self, parent, app, mail, start_idx=-1, no_posts=70):
        super().__init__(parent)

        self.buttons = {}  # Dictionary to store button references
        self.start_idx = start_idx
        self.friends, self.posts = friend_posts_read()
        self.mail = mail
        global temp_idx
        temp_idx = self.start_idx

        # Placeholder profile photo if not provided
        profile_photo = "path/to/default_profile_image.png"  # Change to a valid path

        self.no_posts = no_posts
        self.view_posts_cycle()

    def view_posts_cycle(self):
        global temp_idx
        temp_idx -= 2
        if self.no_posts == 0:
            return
        for friend in self.friends[self.mail]["friends"]:
            # Reset index for the next friend
            self.start_idx = temp_idx

            # Display up to two posts for each friend
            for _ in range(2):
                self.no_posts -= 1
                # Check if there are enough posts
                if (self.start_idx * -1) >= len(self.posts[friend]):
                    break  # No more posts to show for this friend

                # Get the current post for the friend
                post = self.posts[friend][self.start_idx]

                # Create a frame for each post
                request_frame = tk.Frame(self, bd=2, relief=tk.RAISED, padx=10, pady=10, width=300)
                request_frame.pack(fill="x", pady=5, padx=20)

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

                # Move to the next post
                self.start_idx -= 1

            return self.view_posts_cycle()
