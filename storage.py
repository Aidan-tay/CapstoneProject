import sqlite3

def insert(table_name, record: dict):
    """
    Inserts a new record into the table.
    """
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    query = f"INSERT INTO {table_name} VALUES ("

    for key in record.keys():
        query += "?, "

    query = query.rstrip(", ") + ");"

    cur.execute(query, tuple(record.values()))

    conn.commit()
    conn.close()


def update(table_name, record: dict, **kwargs):
    """
    Updates a record in the table that has attributes **kwargs, with a new record.
    Returns None if no matching attributes found. 
    """
    pass

    if find_one(table_name, kwargs) is None:
        return None
    
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    query = f"UPDATE {table_name} SET "

    for key, value in record.items():
        query += f"{key} = {value}, "

    query = query.rstrip(", ") + " WHERE "

    for key, value in kwargs.items():
        query += f"{key} = {value} AND "

    query = query.rstrip(" AND ") + ";"
    cur.execute(query)
    conn.commit()
    conn.close()


def delete(table_name, **kwargs):
    """
    Deletes a record in the table that has attributes **kwargs. 
    """
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    query = f"DELETE FROM {table_name} WHERE "

    for key, value in kwargs.items():
        query += f"{key} = {value} AND "

    query = query.rstrip(" AND ") + ";"
    cur.execute(query)
    conn.commit()
    conn.close()


def find_all(table_name, field=None):
    """
    Returns a list of all the values in 'field' in 'table_name'. 
    If field is None, return a list of dictionaries with the whole table's contents.
    """
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()
    
    if field is None:
        cur.execute(f"SELECT * FROM {table_name}") 
    else:
        cur.execute(f"SELECT {field} FROM {table_name}",)

    records = cur.fetchall()
    all_records = []
    headers = [column[0] for column in cur.description]

    for record in records:
        all_records.append(dict(zip(headers, record)))
    
    conn.close()
    return all_records


def find_one(table_name, **kwargs):
    """
    Returns a record in a dictionary with attributes matching **kwargs.
    Returns None is no such record found. 
    """
    # to fix: does not work for name field only
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    query = f"SELECT * FROM {table_name} WHERE "
    for key, value in kwargs.items():
        query += f"{key} = {value} AND "

    query = query.rstrip(" AND ") + ";"

    try:
        cur.execute(query)
    except sqlite3.OperationalError:   # record not found
        return None

    record = cur.fetchone()
    headers = [column[0] for column in cur.description]
    output = dict(zip(headers, record))

    conn.close()
    return output


def latest_id(table_name):
    """
    Returns the largest id in the table. 
    """
    conn = sqlite3.connect("project uwu.db")
    cur = conn.cursor()

    cur.execute(f"SELECT MAX(id) FROM {table_name}")
    latest_id = cur.fetchone()

    conn.commit()
    conn.close()

    return latest_id[0]
