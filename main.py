import tkinter as tk
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

FONT = ("Roboto", 16)


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    no_of_letters = randint(8, 10)
    no_of_symbols = randint(2, 4)
    no_of_numbers = randint(2, 4)

    password_list = [choice(letters) for _ in range(no_of_letters)]
    password_list.extend([choice(symbols) for _ in range(no_of_symbols)])
    password_list.extend([choice(numbers) for _ in range(no_of_numbers)])

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, string=password)
    pyperclip.copy(password)


def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading existing data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Appending the new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving the updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)


def search_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            # Reading existing data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f"{website}", message=f"Email: {email}\n"
                                                            f"Password: {password}")
        else:
            messagebox.showerror(title="Oops", message=f"No details for {website} exists.")


window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = tk.Canvas(width=200, height=200, highlightthickness=0, bg="white")
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Website
website_label = tk.Label(text="Website:", bg="white")
website_label.grid(row=1, column=0)

website_entry = tk.Entry(width=31)
website_entry.grid(row=1, column=1)
website_entry.focus()

search_button = tk.Button(text="Search", command=search_password, relief="flat", width=14,
                          borderwidth=0, highlightthickness=0, bg="white")
search_button.grid(row=1, column=2)

# Email
email_label = tk.Label(text="Email/Username:", bg="white")
email_label.grid(row=2, column=0)

email_entry = tk.Entry(width=48)
email_entry.insert(0, string="example@email.com")
email_entry.grid(row=2, column=1, columnspan=2)

# Password
password_label = tk.Label(text="Password:", bg="white")
password_label.grid(row=3, column=0)

password_entry = tk.Entry(width=31)
password_entry.grid(row=3, column=1)

generate_password_button = tk.Button(text="Generate Password", command=generate_password, relief="flat",
                                     borderwidth=0, highlightthickness=0, bg="white")
generate_password_button.grid(row=3, column=2)

add_password_button = tk.Button(text="Add", width=43, command=save_password, relief="flat",
                                borderwidth=0, highlightthickness=0, bg="white")
add_password_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
