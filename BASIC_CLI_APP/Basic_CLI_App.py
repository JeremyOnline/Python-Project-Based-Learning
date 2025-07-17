import os
import time


BASE_DIR = os.path.dirname(__file__)
USERS_DATABASE = os.path.join(BASE_DIR, "users-CLI.txt")



# Print Out the Database
def UserDB_Out():
    users = []
    if os.path.exists(USERS_DATABASE):
        with open(USERS_DATABASE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                users.append((username, password))
    return users

# Register New User 
def UserDB_Register():
    username = input("Enter New Username : ")
    password = input("Enter New Password : ")

    users = UserDB_Out()
    for user in users:
        if user[0] == username:
            print("Username already taken!")
            return

    SaveUser(username, password)
    print("Registration Succesful!")

# Save New User to Database
def SaveUser(username, password):
    with open(USERS_DATABASE, "a") as file:
        file.write(f"{username},{password}\n")

# Login into existing user
def UserDB_Login():
    username = input("Username: ").strip() # To prevent blank spaces
    password = input("Password: ").strip()

    users = UserDB_Out()
    for user in users:
        if user[0] == username & pass[0] == password:
            print("Login Succesful")
            return True
    print("Login failed. Incorrect Username or Password")

# Main Menu
def main():
    while True:
        os.system('cls')
        print("\n=====BASIC CLI APP=====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose option (1/2/3): ")

        if choice == "1":
            UserDB_Register()
        elif choice == "2":
            UserDB_Login()
        elif choice == "3":
            print("Goodbye!")
            for i in range(5, 0, -1):
                print(f"Exiting in {i} seconds...")
                time.sleep(1)
            break
        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()

    



