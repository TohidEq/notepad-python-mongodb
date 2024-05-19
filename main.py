import pymongo
from hashlib import sha256

from bson.objectid import ObjectId
import datetime

# baraye namayesh rahat tar list o dict o ...
# dumps(list, indent=4) 4-> tedad space ha baraye har scope
from bson.json_util import (
    dumps,
)

# === CONFIGS ===
# your mongodb URI (open compass, coppy what u see in URI input and paste it. EZ)
MONGO_URI = "mongodb://superuser:12345678@localhost:27017/?authSource=admin"
# you can change values to any string (without " " and symbols pls...)
# your DB name
DB_NAME = "notepadtest"
# your users collection name
COL_USERS_NAME = "userstest"
# your notes collection name
COL_NOTES_NAME = "notestest"


# connecting to db
myClient = pymongo.MongoClient(MONGO_URI)
myDB = myClient[DB_NAME]

myUsers = myDB[COL_USERS_NAME]
myNotes = myDB[COL_NOTES_NAME]
"""
to ez undrestand:
myUsers:[
    {
        id: UID,
        username: str,
        password: str
    }, ...
]

myNotes:[
    {
        id: UID,
        user_id: UID,
        text: str,
        created_at,
        updated_at
    }, ...
]
"""


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


def main():
    user_id = None
    while user_id == None:
        print("bolbol :)")


if __name__ == "__main__":
    main()
