from db import Database

database = Database()


def get_user_by_id_api(user_id):
    return database.retrieve_single("SELECT * FROM \"user\" u WHERE u.user_id=%s", (user_id,))


def get_user_profile_by_user_id_api(user_id):
    return database.retrieve_single("SELECT * FROM user_profile p WHERE p.user_id=%s", (user_id,))


def get_user_by_username_api(username):
    return database.retrieve_single("SELECT * FROM \"user\" u WHERE u.username=%s", (username,))


def get_username_by_id_api(user_id) -> str:
    return database.retrieve_single("SELECT username FROM \"user\" u WHERE u.user_id=%s", (user_id,)).get('username')


def get_password_by_username_api(username: str) -> str:
    return database.retrieve_single("SELECT password FROM \"user\" u WHERE u.username=%s", (username,)).get('password')


def get_user_id_by_username_api(username: str) -> int:
    return database.retrieve_single("SELECT user_id FROM \"user\" u WHERE u.username=%s", (username,)).get('user_id')


def add_user_api(username: str, hash_password: str):
    return database.insert_row(
        "INSERT INTO \"user\"(username, password) VALUES (%s, %s) RETURNING user_id", (username, hash_password,))


def add_new_user_profile_api(user_id, firstname, lastname, phone_number):
    return database.insert_row(
        "INSERT INTO user_profile(user_id, firstname ,lastname, phone_contact) VALUES (%s, %s, %s, %s) RETURNING "
        "user_profile_id",
        (user_id, firstname, lastname, phone_number,))


def delete_account_api(user_id):
    return database.delete_row("DELETE FROM \"user\" u WHERE u.user_id=%s", (user_id,))
