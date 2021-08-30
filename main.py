from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# Program: main.py
# Project: Password Generator and Manager
# Purpose: Facilitates creation and use of random passwords for any number of websites
# Author:  Thomas Franz wrote this instance! This is part of Angela Yu's 100 Days of Code course on Udemy

# Function: generate_password
# Purpose:  Creates a completely random password
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# Function: save
# Purpose:  Saves the set of credentials to a local file
def save():

    website = website_entry.get()
    name = name_entry.get()
    password = password_entry.get()
    new_json_data = {
        website: {
            "name": name,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="All fields are mandatory!", message="Please fill out all fields before saving!")
    else:
        try:                        # Try to open the existing file
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:   # If we couldn't open an existing file
                with open("data.json", "w") as data_file:   # Create a new file
                    json.dump(new_json_data, data_file, indent=4)   # Write json info to the file
        else:
            data.update(new_json_data)  # Updating existing file with new data

            with open("data.json", "w") as data_file:   # Write json info to the file
                    json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
        messagebox.showinfo(title=website, message=f"  Saved! \nWebsite: {website} \nEmail: {name} "
                                                   f"\nPassword: {password}")


# Function: find_password
# Purpose:  Attempts to find the password and sign-in name associated with the given website in the data file
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            name = data[website]["name"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Username: {name}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# --------
# UI Setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=250)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(150, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
name_label = Label(text="Username:")
name_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
name_entry = Entry(width=39)
name_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
