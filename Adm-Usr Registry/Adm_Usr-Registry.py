"""
Study Case: Gym System
Admin & User Login
Track User Time
Membership(Start date, End date, Expiry)

"""

import os
import datetime

def reg_new_member():
    # Create a new member
    member_reg = input("Input your name: ")
    print(member_reg)

def login_member():
    member_login = input("Input your name: ")

reg_new_member()

def operation():
    while True:
        
