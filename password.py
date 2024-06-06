#password manager
from cryptography.fernet import Fernet

def write_key():
    key = Fernet.generate_key() 
    with open("key.key", "wb") as key_file: 
        key_file.write(key)  
                              
def load_key():
    with open("key.key", "rb") as file:
        key = file.read()
    return key

while True:
    mass_pwd = input("Enter the master password: ")
    if mass_pwd == "@Hiipython":
        print("Welcome")
        break
    else:
        print("Invalid Password")

key = load_key() # type: ignore
fer = Fernet(key)  # type: ignore

def view():
    try:
        with open('password.txt','r') as f:  
            for line in f.readlines():
                data = line.rstrip()
                if "-" in data:
                    user, passw = data.split(" - ")
                    print("User:", user, "Password:", fer.decrypt(passw.encode()).decode() + "\n")
                else:
                    print("Data not found",line)
    except FileNotFoundError:
        print("The file 'password.txt' does not exist.")

def check_password(password): # type: ignore
    has_upper = any(char.isupper() for char in password) # type: ignore
    has_lower = any(char.islower() for char in password) # type: ignore
    has_number = any(char.isdigit() for char in password) # type: ignore
    has_special = any(not char.isalnum() for char in password) # type: ignore

    if not has_upper:
        print("Password is missing uppercase characters.")
    elif not has_lower:
        print("Password is missing lowercase characters.")
    elif not has_number:
        print("Password is missing numbers.")
    elif not has_special:
        print("Password is missing special characters.")
    else:
        print("Password is all good")

def add():
    name = input('Username:')
    username_exists = False
    with open('password.txt', 'r') as f: 
        for line in f:
            user = line.split("-", 1)[0].strip()
            if name == user:
                username_exists = True
                break
    if username_exists:
        print("Username already exists.")
        return
    password = input('Password:') 
    check_password(password)
    with open('password.txt', 'a') as f:
        f.write(name + " - " + fer.encrypt(password.encode()).decode() + "\n") 
        print("Password added successfully")

def change():
    name = input('Enter the username to change the exsiting password: ')
    with open('password.txt', 'r') as f:
        lines = f.readlines()
        
    with open('password.txt', 'w') as f:
        for line in lines:
            user, passw = line.split(" - ", 1) # type: ignore
            if user.strip() == name:
                new_password = input('Enter the new password: ')
                check_password(new_password)
                f.write(user + " - " + fer.encrypt(new_password.encode()).decode() + "\n")
                print("Password changed successfully")
            elif user.strip() != name:
                print("Username Not Found")
            else:
                f.write(line)

while True:
    mode = input("Would you like to add a new password or view the existing one or change a password( view, add, change) and to quit press q- ").lower()
    if mode == "q":
        print("Your changes are saved!")
        break
    if mode == "view":
        view()
    elif mode == "add":
        add()
    elif mode == "change":
        change()
    else:
        print("Invalid mode")
        continue