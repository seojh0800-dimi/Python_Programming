import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nowhere.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area_name TEXT NOT NULL UNIQUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area_name TEXT NOT NULL,
                congestion_level TEXT,
                checked_at TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_history(items):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in items:
            cur.execute(
                "INSERT INTO search_history (area_name, congestion_level, checked_at) VALUES (?, ?, ?)",
                (item["area_name"], item["congestion_level"], checked_at),
            )
        conn.commit()
    finally:
        conn.close()


def load_history():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT checked_at, area_name, congestion_level
            FROM search_history
            ORDER BY id DESC
            LIMIT 30
        """)
        return cur.fetchall()
    finally:
        conn.close()


def add_favorite(area_name):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO favorites (area_name) VALUES (?)",
            (area_name,),
        )
        conn.commit()
    finally:
        conn.close()


def load_favorites():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT area_name FROM favorites ORDER BY id DESC")
        rows = cur.fetchall()

        favorites = []
        for row in rows:
            favorites.append(row[0])
        return favorites
    finally:
        conn.close()


def delete_favorite(area_name):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM favorites WHERE area_name = ?", (area_name,))
        conn.commit()
    finally:
        conn.close()
