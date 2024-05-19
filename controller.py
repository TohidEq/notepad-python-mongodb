import pymongo
from hashlib import sha256

from bson.objectid import ObjectId
import datetime

# baraye namayesh rahat tar list o dict o ...
# dumps(list, indent=4) 4-> tedad space ha baraye har scope
from bson.json_util import (
    dumps,
)

import config

# connecting to db
myClient = pymongo.MongoClient(config.MONGO_URI)
myDB = myClient[config.DB_NAME]

myUsers = myDB[config.COL_USERS_NAME]
myNotes = myDB[config.COL_NOTES_NAME]


# ----------------
# ---- users -----
def not_exist_in_users(username: str) -> bool:
    query = {"username": username}
    document = myUsers.find_one(query)
    if not document:  # if ducoment is EMPTY
        return True
    return False


def encode_password(password: str) -> str:
    encoded_str = sha256(password.encode("utf-8")).hexdigest()
    return encoded_str


def check_password(password: str, encoded_password: str) -> bool:
    if encode_password == encode_password(password):
        return True
    return False


def create_new_user(username: str, password: str) -> bool:
    if not_exist_in_users(username):
        encoded_password = encode_password(password)
        new_user_query = {"username": username, "password": encoded_password}
        insert = myUsers.insert_one(new_user_query)

        # check success
        if insert.inserted_id:
            print(
                f"new user inserted, insert id:[{insert.inserted_id}]"
            )  # u can delete this line
            return True
    print(
        f"insert faild, or this username[{username}] exists"
    )  # u can delete this line
    return False


# ----------------
# ---- notes -----
def get_all_user_notes(user_id: ObjectId) -> list:
    finding_user_notes_query = {"user_id": user_id}
    user_notes = myNotes.find(finding_user_notes_query)
    return list(user_notes)


def create_new_note(user_id: ObjectId, text: str) -> bool:
    now_date = datetime.datetime.now()
    new_note_query = {
        "user_id": user_id,
        "text": text,
        "created_at": now_date,
        "updated_at": now_date,
    }

    insert = myNotes.insert_one(new_note_query)

    # check success
    if insert.inserted_id:
        print(
            f"new note inserted, insert id:[{insert.inserted_id}]"
        )  # u can delete this line
        return True
    print(f"insert faild")  # u can delete this line
    return False


def update_note(note_id: ObjectId, text) -> bool:
    now_date = datetime.datetime.now()
    finding_note_query = {"_id": note_id}
    update_note_query = {
        "$set": {
            "text": text,
            "updated_at": now_date,
        }
    }
    update = myNotes.update_one(finding_note_query, update_note_query)

    # check success
    if update.modified_count:
        print(f"note updated")  # u can delete this line
        return True
    print(f"note update faild")  # u can delete this line
    return False


def update_note(note_id: ObjectId) -> bool:
    finding_note_query = {"_id": note_id}
    delete = myNotes.delete_one(finding_note_query)

    # check success
    if delete.deleted_count:
        print(f"note deleted")  # u can delete this line
        return True
    print(f"note delete faild")  # u can delete this line
    return False
