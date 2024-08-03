import sqlite3

db = sqlite3.connect("data.db")
cr = db.cursor()

cr.execute(
"""
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    email TEXT UNIQUE,
    password TEXT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted DATETIME)
"""
)

cr.execute(
"""
    CREATE TABLE IF NOT EXISTS admins(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    email TEXT UNIQUE,
    password TEXT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted DATETIME)
"""
)