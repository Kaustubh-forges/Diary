# -----------Importing Necessary Modules----------
from tkinter import *  # Importing all Tkinter widgets for GUI creation
from tkinter import messagebox  # Importing messagebox separately for popup dialogs
import bcrypt  # For secure password hashing and checking
import day_time  # Custom module providing current day/time for entries
import json  # To store and retrieve diary data and passwords in JSON format
from tkinter import Scrollbar  # Separate import for scrollbars in the GUI

# ----------Constant Variables----------
FONT = ("TIMES NEW ROMAN", 36, "bold")  # Default font used across the UI
COUNT_OF_ENTRIES = 0  # Counter to keep track of number of diary entries

# ----------Setting up Main Window----------
window = Tk()  # Initialize the main Tkinter window
window.title("Secret Diary")  # Window title
window.minsize(height=500, width=800)  # Minimum window size


# ----------Function for Loading and Checking Entered Password----------
def check_password():
    """
    Verifies if the password entered by the user matches the stored hashed password.
    Uses bcrypt for secure hash comparison.
    """
    try:
        # Try to open the password file
        file = open("password_file.json", "r")
        data = json.load(file)  # Load stored password from JSON
    except FileNotFoundError:
        # If no password file exists, show warning message
        message_for_no_file = messagebox.showwarning(
            title="Warning Message!",
            message="You have no previous entries saved."
        )
    else:
        # Get stored hashed password and encode it to bytes for bcrypt
        hashed_version = data["Password"].encode("utf-8")
        # Check if entered password matches stored hash
        if bcrypt.checkpw(current_password_entry.get().encode("utf-8"), hashed_version):
            # If correct, remove password input widgets and show common diary UI
            current_password_entry.destroy()
            current_password_label.destroy()
            current_password_button.destroy()
            showing_common_ui()
        else:
            # If incorrect, show warning popup
            message_wrong_password = messagebox.showwarning(
                title="Warning Message!",
                message="The entered password is incorrect!"
            )


# ----------Function for Displaying Common Diary UI----------
def showing_common_ui():
    """
    Displays the main diary interface after password verification or first-time password setup.
    This UI is shared between first-time users and returning users.
    """
    window.geometry("800x630")  # Resize main window for diary view
    canvas.place(x=270, y=0)  # Place main canvas (decorative image)
    # Remove introductory/decoration widgets
    decoration_label1.destroy()
    decoration_label2.destroy()
    canvas2.destroy()
    canvas3.destroy()
    # Place diary entry-related widgets
    diary_entry_check_entries.place(x=10, y=100)

    # Display current date and time from day_time module
    Date = Label(
        window,
        text=f"Date & Time of Entry: {day_time.split_obj[0]}|{day_time.split_obj[1]}",
        font=("TIMES NEW ROMAN", 30, "bold"),
        highlightcolor="#4CAF50",
        highlightthickness=1,
        highlightbackground="#4CAF50"
    )
    Date.place(x=0, y=320)

    # Place other diary widgets
    diary_entry_button.place(x=315, y=250)
    diary_entry_label.place(x=0, y=400)
    diary_entry.place(x=150, y=390)


# -----------Function for First-Time Users to Set Password----------
def first_password():
    """
    Sets a new password for first-time users.
    Hashes the password using bcrypt and saves it in JSON.
    """
    try:
        file = open("password_file.json", "r")
    except FileNotFoundError:
        # If no password exists, hash and save the entered password
        password = Password_entry.get()
        hashed_version = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        hashed_string = hashed_version.decode("utf-8")
        with open("password_file.json", "w") as pass_file:
            json.dump({"Password": hashed_string}, pass_file)
        # Remove password setup UI and show main diary UI
        Password.destroy()
        Password_entry.destroy()
        Password_entry_button_for_first_entry.destroy()
        showing_common_ui()
    else:
        # If password already exists, show a warning
        file_exists = messagebox.showwarning(
            title="Warning Message!",
            message="You have created a password previously."
        )


# ----------Function to Add Diary Entry----------
def add_entry():
    """
    Adds a diary entry to the Entries.json file.
    Stores data in dictionary format with date, time, and content.
    Creates a key-tracking file (Keys.txt) to maintain count.
    """
    global COUNT_OF_ENTRIES
    COUNT_OF_ENTRIES += 1
    # Append entry count to Keys.txt (used as simple counter)
    with open("Keys.txt", "a+") as file:
        file.write(str(COUNT_OF_ENTRIES) + "\n")

    file = open("Keys.txt", "r")
    data = {
        "Entry " + str(len(file.readlines())): {
            "Day": day_time.day,
            "Time": day_time.split_obj[1],
            "Entry": diary_entry.get("1.0", END)  # Get text from Text widget
        }
    }
    file.close()

    # Check if user entered anything
    if diary_entry.get("1.0", END) == "":
        empty_field_message = messagebox.showwarning(
            title="Warning Message!",
            message="You left one of the fields empty."
        )
    else:
        # Try to read previous entries
        try:
            with open("Entries.json", "r") as file:
                old_data = json.load(file)
        except FileNotFoundError:
            # If no entries exist, create new file
            with open("Entries.json", "w") as file:
                json.dump(data, file, indent=4)
        else:
            # Update old data with new entry
            old_data.update(data)
            with open("Entries.json", "w") as file:
                json.dump(old_data, file, indent=4)


# ----------Function to Show Previous Entries in Scrollable Window----------
def show_entries_window():
    """
    Opens a new top-level window displaying all previous diary entries.
    Uses a scrollable Text widget to handle multiple entries.
    """
    new_window = Toplevel(window)
    new_window.title("Secrets of the Past")

    # Add vertical scrollbar
    scroll_bar = Scrollbar(new_window)
    scroll_bar.configure(highlightcolor="light grey", highlightbackground="light grey")
    scroll_bar.pack(side="right", fill="y")

    # Text widget to display entries
    text = Text(
        new_window,
        width=100,
        height=20,
        font=("TIMES NEW ROMAN", 14, "normal"),
        relief="flat",
        highlightthickness=1,
        highlightcolor="#4CAF50",
        highlightbackground="#4CAF50",
        wrap="word",
        yscrollcommand=scroll_bar.set  # Connect scrollbar to text widget
    )
    text.pack(fill="both", expand=True)

    # Load entries from JSON and insert into Text widget
    with open("Entries.json", "r") as file:
        content = json.load(file)

    for key in content:
        text.insert(END, key + "\n")
        text.insert(END, "Day: " + content[key]["Day"] + "\n" +
                    "Time: " + content[key]["Time"] + "\n" +
                    "Entry: " + content[key]["Entry"] + "\n")

    text.configure(state="disabled")  # Make Text widget read-only
    scroll_bar.configure(command=text.yview)  # Connect scrollbar to text scroll


# ----------Setting up the Canvas----------
canvas = Canvas(height=300, width=400, background="gray12", highlightthickness=0)
image = PhotoImage(file="New_Diary.png")
for_image = canvas.create_image(100, 150, image=image)

# ----------New Password UI Widgets----------
Password = Label(
    window,
    text="New Password: ",
    font=FONT,
    highlightcolor="#4CAF50",
    highlightthickness=1,
    highlightbackground="#4CAF50"
)
Password_entry = Entry(
    window,
    width=80,
    highlightthickness=1,
    highlightcolor="#4CAF50",
    highlightbackground="#4CAF50",
    relief="flat",
    font=("TIMES NEW ROMAN", 14, "normal")
)
Password_entry_button_for_first_entry = Button(
    window,
    text="Save Password",
    font=("TIMES NEW ROMAN", 18, "normal"),
    borderwidth=5,
    command=first_password,
    padx=50
)
Password_entry_button_for_first_entry.configure(height=0)
Password_entry.configure(highlightthickness=3)

# ----------Current Password UI Widgets----------
current_password_label = Label(
    window,
    text="Current Password: ",
    font=FONT,
    highlightcolor="#4CAF50",
    highlightthickness=1,
    highlightbackground="#4CAF50"
)
current_password_entry = Entry(
    window,
    width=80,
    relief="flat",
    highlightthickness=1,
    highlightcolor="#4CAF50",
    highlightbackground="#4CAF50",
    font=("TIMES NEW ROMAN", 14, "normal")
)
current_password_button = Button(
    window,
    text="Check Password",
    font=("TIMES NEW ROMAN", 18, "normal"),
    command=check_password,
    borderwidth=5
)
current_password_button.configure(height=0)
current_password_entry.configure(highlightthickness=3)

# ----------Diary Entry UI Widgets----------
diary_entry_label = Label(
    window,
    text="Entry:",
    font=FONT,
    highlightcolor="#4CAF50",
    highlightthickness=1,
    highlightbackground="#4CAF50"
)
diary_entry = Text(
    window,
    width=60,
    height=10,
    font=("TIMES NEW ROMAN", 14, "normal"),
    relief="flat",
    highlightthickness=1,
    highlightcolor="#4CAF50",
    highlightbackground="#4CAF50",
    wrap="word"
)
diary_entry_button = Button(window, text="Add entry", font=("TIMES NEW ROMAN", 18, "normal"), command=add_entry)
diary_entry_check_entries = Button(window, text="View Previous Entries", font=("TIMES NEW ROMAN", 18, "normal"),
                                   command=show_entries_window)

# ----------Decorative Labels and Images----------
decoration_label1 = Label(
    text="Oh great Magician! It's time to create your very own spell\n...or password in lame words.",
    font=("French Script MT", 36, "bold"),
    background="dodgerblue4",
    foreground="white",
    highlightcolor="cornsilk",
    highlightthickness=1,
    highlightbackground="cornsilk"
)
decoration_label2 = Label(
    text="Welcome back, Magician! Enter the correct password\n... or be at the risk of being bludgeoned by an ugly mountain troll.",
    font=("French Script MT", 36, "bold"),
    background="dodgerblue4",
    foreground="white",
    highlightcolor="cornsilk",
    highlightthickness=1,
    highlightbackground="cornsilk"
)

canvas2 = Canvas(height=100, width=100)
image2 = PhotoImage(file="Wizard.png")
for_image2 = canvas2.create_image(50, 50, image=image2)

canvas3 = Canvas(height=100, width=100)
image3 = PhotoImage(file="Troll.png")
for_image3 = canvas3.create_image(50, 50, image=image3)


# ----------Function for Asking if User is Returning----------
def ask_start_question():
    """
    Prompt user to check if they have previous entries.
    Adjust UI based on user's response.
    """
    start_question = messagebox.askyesno(title="Question Box", message="Have you made entries before?")
    window.configure(background="gray12")
    if start_question:
        # Returning user: prompt password
        decoration_label2.place(x=0, y=50)
        window.configure(highlightthickness=5, highlightcolor="light grey", highlightbackground="light grey")
        window.geometry("1000x500")
        canvas3.place(x=405, y=360)
        current_password_entry.focus()
        current_password_label.place(x=262, y=180)
        current_password_entry.place(x=110, y=260)
        current_password_button.place(x=365, y=300)
    else:
        # First-time user: prompt password creation
        window.configure(highlightthickness=5, highlightcolor="light grey", highlightbackground="light grey")
        window.geometry("903x500")
        Password_entry.focus()
        canvas2.place(x=410, y=370)
        decoration_label1.place(x=0, y=50)
        Password.place(x=290, y=180)
        Password_entry.place(x=80, y=260)
        Password_entry_button_for_first_entry.place(x=320, y=300)


# ----------Start Application----------
window.after(100, ask_start_question)  # Delay execution to allow window setup
window.mainloop()  # Start Tkinter event loop

#'