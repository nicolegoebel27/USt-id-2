import sqlite3
import time


class VATCache:

    def __init__(self):
        self.conn = sqlite3.connect("cache.db", check_same_thread=False)
        self._init()

    def _init(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            vat TEXT PRIMARY KEY,
            data TEXT,
            ts INTEGER
        )
        """)
        self.conn.commit()

    def get(self, vat):
        c = self.conn.cursor()
        c.execute("SELECT data FROM cache WHERE vat=?", (vat,))
        row = c.fetchone()

        if row:
            import ast
            return ast.literal_eval(row[0])
        return None

    def set(self, vat, data):
        c = self.conn.cursor()
        c.execute(
            "REPLACE INTO cache VALUES (?, ?, ?)",
            (vat, str(data), int(time.time()))
        )
        self.conn.commit()
