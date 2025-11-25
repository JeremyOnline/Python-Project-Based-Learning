import os
"""
Program yang dapat menerima masukan nama,
tempat-tanggal lahir, 
nim mahasiswa, 
dan rata-rata nilai
"""

def halo():
    nama_mahasiswa = input("Nama Mahasiswa: ")
    nim = input("Masukkan NIM(xxxxxx): ")
    while True:
        if nim == "tes":
            print("OK")
            break
        else:
            print("incorrect")
            break
            
halo()
    