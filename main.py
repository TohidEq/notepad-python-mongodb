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


# returns dict { "number":ObjectId }
def show_all_notes(user_id: ObjectId) -> dict:
    notes_choice_dict = {}
    index_counter = 1
    notes = controller.get_all_user_notes(user_id)
    if len(notes):  # if we have notes
        for note in notes:
            notes_choice_dict[str(index_counter)] = note["_id"]
            print(
                f"""-------------------------------------
                \r{index_counter}. {note["text"]}
                \r created: {note["created_at"]}
                \r updated: {note["updated_at"]} """
            )
            index_counter += 1
    return notes_choice_dict


def manage_notes(notes_choice_dict: dict) -> bool:
    print("Enter note number (0 to exit) >>")
    note_choice = input(">> ")
    if note_choice in notes_choice_dict:
        note_id = notes_choice_dict[note_choice]
        print(menu_after_select_note)
        menu_choice = int(input("(0 to exit) >> "))
        match menu_choice:
            case 0:
                return True
            case 1:  # edit
                new_text = input("enter new note text >>")
                controller.update_note(note_id, new_text)
                return True
            case 2:  # delete
                controller.delete_note(note_id)
                return True
    return True


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
                        notes_choice_dict = show_all_notes(user_id)
                        manage_notes(notes_choice_dict)

                    case _:
                        print("enter 1 or 2 pls")
                input()


if __name__ == "__main__":
    main()
