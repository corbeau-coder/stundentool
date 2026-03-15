import sqlite3

from src.modules.sqlite.db import DatabaseHandler

def test_init_db(monkeypatch):
    