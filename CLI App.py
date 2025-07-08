# Ini adalah program CLI (Command Line Interface) menggunakan user registration
"""
✅ Tasks:
Create menu() function (register / login / exit).
Baru/Login/Exit

Register:

Input username & password.
Masukkan Username dan password

Save to users.txt as username,password.
Save ke file User sebagai Username, password

Login:

Read from users.txt and verify credentials.
Baca dari file User dan verifikasi kreditensial.

Use lists and string manipulation to parse .txt lines.
Gunakan daftar dan manipulasi string untuk memisahkan baris .txt.

Bonus: Mask password input (getpass.getpass())
"""

import os


DATABASE_USER = "D:\Coding\Python\Project\CLI APP/users.txt"

# Menaruh users yang sudah terdaftar di dalam file ke dalam list
def user_baru_masuk():
    users = []
    if os.path.exists(DATABASE_USER):
        with open(DATABASE_USER, "r") as file:
            for baris in file:
                username, password = baris.strip().split(",")
                users.append((username,password))
    return users

# Save User Baru ke file
def save_user(username, password):
    with open(DATABASE_USER, "a") as file:
        file.write(f"{username},{password}\n")

# Register User baru!
def register():
    username = input("Masukkan Username baru: ").strip()
    password = input("Masukkan Password baru: ").strip()

    users = user_baru_masuk()
    for user in users:
        if user[0] == username:
            print("Username udah dipakai Bro!")
            return
        
    save_user(username, password)
    print("User baru berhasil ditambahkan!")
















# Beranda Utama
def utama():
    while True:
        print("\n==== BASIC CLI APP ====")
        print("Coba lu input lok jem, ini baru fitur registrasi (7/7/25) : ")
        choice = input("1/3: ")

        if choice == "1":
            register()
        elif choice == "3":
            print("Goodbye!")
            break


    os.system("cls")



if __name__ == "__main__":
    os.system("cls")
    utama()







# Kenapa Harus __name__?
#Karena __name__ adalah built-in variable (variabel khusus) yang selalu tersedia di setiap file Python secara otomatis.