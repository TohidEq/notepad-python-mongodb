import pymongo
from hashlib import sha256

from bson.objectid import ObjectId
import datetime

# baraye namayesh rahat tar list o dict o ...
# dumps(list, indent=4) 4-> tedad space ha baraye har scope
from bson.json_util import (
    dumps,
)

import controller
import os


# define our clear function
def clear():
    # for windows
    if os.name == "nt":
        _ = os.system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system("clear")


menu_welcome = """- Welcome
1. Create new acc
2. Login
"""

menu_after_login = """- Main
1. Create new Note
2. My notes
"""

menu_after_select_note = """- Manage Note
1. Edit
2. Delete
"""


def create_new_acc() -> bool:
    username = input("username >> ")
    password = input("username >> ")
    if controller.not_exist_in_users(username):
        return controller.create_new_user(username, password)
    print(f"this username{username} exists")
    return False


def login() -> ObjectId:
    username = input("username >> ")
    password = input("password >> ")
    if controller.exist_in_users(username):
        encoded_password = controller.get_user_pass(username)
        if controller.check_password(password, encoded_password) == True:
            print("Correct password\nWelcome")
            return controller.get_user_id(username)
        print("Incorrect password")
        return None
    print("user not exist")
    return None


def create_new_note(user_id: ObjectId) -> bool:
    text = input("note text >> ")
    if controller.create_new_note(user_id, text):
        print(f"created")
        return True
    return False


# not completed...
def show_all_notes(user_id: ObjectId):
    notes = controller.get_all_user_notes(user_id)
    if len(notes):
        for note in notes:
            print(note["text"])


def main():
    user_id = None

    while True:
        clear()
        match user_id:
            case None:  # no logged in
                # Clearing the Screen
                print(menu_welcome)
                choice = int(input(">> "))
                match choice:
                    case 1:  # create acc
                        create_new_acc()

                    case 2:  # login
                        user_id = login()
                    case _:
                        print("enter 1 or 2 pls")
                input()
            case _:  # if we logged in
                print(menu_after_login)
                choice = int(input(">> "))
                match choice:
                    case 1:  # create note
                        create_new_note(user_id)

                    case 2:  # see all user notes
                        show_all_notes(user_id)
                    case _:
                        print("enter 1 or 2 pls")
                input()


if __name__ == "__main__":
    main()
