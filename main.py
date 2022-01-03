import tkinter
from tkinter import messagebox
import random
import pyperclip
import os
import json
from encryption import Encryption
from functools import partial
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
key=""
translate = Encryption()



def get_password():
    global key

    def destroy_main(self):
        if key == "":
            window.quit()
    def get_text(self):
        global key
        key = enter_entry.get()
        try:
            with open("data.json","rb") as file:
                to_decrypt=file.read()
                dictionary = translate.decrypt(key,to_decrypt)
        except:
            enter_entry.delete(0,tkinter.END)
            enter_label.config(text="Please enter a valid key!!")
        else:
            manual_key_window.destroy()
            window.deiconify()
    if os.path.exists("[INSERT YOUR PATH HERE]"):
        with open("[INSERT YOUR PATH HERE PLUS FILENAME]") as file:
            key=file.read()
    else:
        window.withdraw()
        manual_key_window = tkinter.Toplevel(window)
        enter_label = tkinter.Label(manual_key_window,text="Key:")
        enter_label.pack()
        enter_label.focus()

        enter_entry = tkinter.Entry(manual_key_window, show="*",width=40)
        enter_entry.bind("<Return>",get_text)
        enter_entry.pack()
        enter_entry.focus_set()
        manual_key_window.bind("<Destroy>",destroy_main)



def search():
    global key

    def search_from_button(entity):
        with open("data.json", "rb") as file:
            to_decrypt = file.read()
            dictionary = translate.decrypt(key, to_decrypt)
        website_entry.delete(0, tkinter.END)
        website_entry.insert(0, entity)
        email_username_entry.delete(0, tkinter.END)
        email_username_entry.insert(0, dictionary[entity]["email"])
        password_entry.delete(0, tkinter.END)
        password_entry.insert(0, dictionary[entity]["password"])
        pyperclip.copy(dictionary[entity]["password"])
        menu.destroy()
    try:
        with open("data.json","rb") as file:
            to_decrypt = file.read()
            dictionary = translate.decrypt(key,to_decrypt)
    except FileNotFoundError:
        messagebox.showerror(title="No existant passwords file", message="Unable to find your request\n"
                                                                         "No file to find passwords")
    else:
        to_find = website_entry.get()
        if to_find in dictionary:
            email_username_entry.delete(0, tkinter.END)
            email_username_entry.insert(0, dictionary[to_find]["email"])
            password_entry.delete(0, tkinter.END)
            password_entry.insert(0, dictionary[to_find]["password"])
            pyperclip.copy(dictionary[to_find]["password"])
        else:
            elements = [key for key in dictionary.keys()]
            elements.sort()
            menu = tkinter.Toplevel(window)
            if len(elements)%4 == 0:
                rows = len(elements)/4
            else:
                rows = (int(len(elements)/4))+1
            counter=0
            for column in range(4):
                try:
                    for row in range(int(rows)):
                        button = tkinter.Button(menu, text=elements[counter], command=partial(search_from_button, elements[counter]))
                        button.grid(row=row, column=column,sticky='w')
                        counter += 1
                except IndexError:
                    pass


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    password_list = [random.choice(letters) for char in range(nr_letters)] + [random.choice(symbols) for char in range(nr_symbols)] + [random.choice(numbers) for char in range(nr_numbers)]
    random.shuffle(password_list)
    password="".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {website:{"email":email,"password":password}}
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Empty fields!!",message="Please don't leave any field blank")
    else:
        is_ok = messagebox.askokcancel(title=website,message=f"These are the details entered: \n"
            f"Email: {email} \nPassword: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json","rb") as file:
                    data = translate.decrypt(key,file.read())
            except FileNotFoundError:
                with open("data.json","w") as file:
                    json.dump(new_data,file,indent=4)
                translate.encrypt(key)
            else:
                data.update(new_data)
                with open("data.json","w") as file:
                    json.dump(data, file)
                translate.encrypt(key)
            finally:
                website_entry.delete(0, tkinter.END)
                email_username_entry.delete(0, tkinter.END)
                email_username_entry.insert(0,"aviladavilam@gmail.com")
                password_entry.delete(0, tkinter.END)
def remove_data():
    global key
    is_ok = messagebox.askokcancel(title="Erasing account!!",message=f"You are going to delete:\n{website_entry.get()}")
    if is_ok:
        try:
            with open("data.json","rb") as file:
                data = translate.decrypt(key, file.read())
        except FileNotFoundError:
            pass
        else:
            key_to_delete = website_entry.get()
            if key_to_delete in data:
                data.pop(key_to_delete)
            with open("data.json","w") as file:
                json.dump(data,file)
            translate.encrypt(key)

# ---------------------------- UI SETUP ------------------------------- #
#os.chdir(__file__.replace("/main.py",""))
window = tkinter.Tk(className='myPasswordManagerApp')
window.config(padx=20,pady=20)
window.title("Password Manager")

imagen = tkinter.PhotoImage(file="logo.png")
canvas = tkinter.Canvas(width=200,height=200)
canvas.create_image(100,100,image=imagen)
canvas.grid(row=0,column=1)

website_label = tkinter.Label(text="Website:")
website_label.grid(row=1,column=0)

website_entry = tkinter.Entry(width=40)
website_entry.grid(row=1,column=1,sticky="W")
website_entry.focus()

search_button =tkinter.Button(text="Search",width=14,command=search)
search_button.grid(row=1,column=2)

email_username_label = tkinter.Label(text="Email/Username:")
email_username_label.grid(row=2,column=0)

email_username_entry = tkinter.Entry(width=58)
email_username_entry.grid(row=2,column=1,columnspan=2,sticky="W")
email_username_entry.insert(0,"aviladavilam@gmail.com")

password_label = tkinter.Label(text="Password:")
password_label.grid(row=3,column=0)

password_entry = tkinter.Entry(width=40)
password_entry.grid(row=3,column=1,sticky="W")

generate_button = tkinter.Button(text="Generate Password",width=14,command=generate_password)
generate_button.grid(row=3,column=2,sticky="W")

remove_button=tkinter.Button(text="Remove",width=12,bg="red",command=remove_data)
remove_button.grid(row=4,column=0)
add_button = tkinter.Button(text="Add",width=40,bg="green",command=save_data)
add_button.grid(row=4,column=1,columnspan=2)

get_password()
window.mainloop()
