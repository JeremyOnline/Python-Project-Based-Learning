import os
import sqlite3
import time
import datetime

"""
Study Case:
We have a gym, and we want to track how long each person spends their time in the gym.

1. We make a system that tracks the time each person enters and exits the gym.
2. By typing their name into the system, with the datetime, and of course, the time.
3. We track the time when the name is type into the system.
4. Also i will make database for user that already become a member, so that we can track our member!

"""

BASE_DIR = os.path.dirname(__file__)
USERS_DATABASE = os.path.join(BASE_DIR, "Duration_Registration.txt")

# Print Out the Database
def database_out():
    users = []
    if os.path.exists(USERS_DATABASE):
        with open(USERS_DATABASE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                users.append((username, password))
    return users

# Save New User to Database
def saveUser(name, time_user):
    with open(USERS_DATABASE, "a") as file:
        file.write(f"{name},{time_user}\n")

# transaksi = {
#             'deskripsi': deskripsi,
#             'section': section,
#             'jenis': jenis,
#             'jumlah': jumlah,
#             'tanggal': tanggal
#         }
        

def user_In(name, time_user):
    print(f"Welcome {name}!, You entered at {time_user}")
    saveUser(name, time_user)

def user_out(name, time_user):
    print(f"See you again, {name}")

def main():
    while True:
        print("\n1. Enter the gym")
        print("2. Exit the gym")
        print("3. Check member")
        print("4. Exit the program")
        choice = input("What would you like to do? ")

        if choice == "1":
            name = input("What is your name? : ").capitalize()
            time_user = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_In(name, time_user)
        elif choice == "2":
            name = input("What is your name? ").capitalize()
            time_user = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_out(name, time_user)
        elif choice == "4":
            print("Goodbye!, See you again , Admin")
            for i in range(5, 0, -1):
                print(f"Exiting in {i} seconds...")
                time.sleep(1)
            break

main()
