import sqlite3

def insert(table_name, record):
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO ? (?)
                VALUES (?);
                """, tuple(table_name) + tuple(record.keys()) + tuple(record.values()))

    conn.commit()
    conn.close()


def update(table_name, record, **kwargs):
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    cur.execute("""
                """)

    conn.commit()
    conn.close()


def delete(table_name, **kwargs):
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    cur.execute("""
                """)

    conn.commit()
    conn.close()


def findall(table_name, field=None):
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    cur.execute("""
                """)

    conn.commit()
    conn.close()


def findone(table_name, **kwargs):
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    cur.execute("""
                """)

    conn.commit()
    conn.close()

