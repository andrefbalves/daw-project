import sqlite3

from flask import current_app

from models import User


def get_connection():
    connection = sqlite3.connect(current_app.config["DATABASE_PATH"])
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                full_name TEXT,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )
        existing_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(users)")
        }

        if "full_name" not in existing_columns:
            connection.execute("ALTER TABLE users ADD COLUMN full_name TEXT")

        if "email" not in existing_columns:
            connection.execute("ALTER TABLE users ADD COLUMN email TEXT")


def create_user(username, password_hash, full_name=None, email=None):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (username, full_name, email, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (username, full_name, email, password_hash),
        )
        return User(
            id=cursor.lastrowid,
            username=username,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
        )


def get_user_by_username(username):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, username, full_name, email, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    return User.from_row(row)


def get_user_by_id(user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, username, full_name, email, password_hash
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    return User.from_row(row)
