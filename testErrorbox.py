import tkinter as tk
from tkinter import messagebox

def display_error_message(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    messagebox.showerror("Error", message)

    # This is optional, but it's a good practice to close the main window
    # when the messagebox is closed to prevent the application from hanging.
    root.destroy()

# Example usage:
error_message = "This is an error message."
display_error_message(error_message)