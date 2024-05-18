import pymongo
from hashlib import sha256

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
        query = {"username": username, "password": encoded_password}
        insert = myUsers.insert_one(query)
        if insert.inserted_id:
            print(
                f"inserted, insert id:[{insert.inserted_id}]"
            )  # u can delete this line
            return True

    print(
        f"insert faild, or this username[{username}] exists"
    )  # u can delete this line
    return False
