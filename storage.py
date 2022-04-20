import sqlite3

def insert(table_name, record):
    """
    Inserts a new record into the table.
    """
    
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    query = f"INSERT INTO {table_name} VALUES ("

    for key in record.keys():
        query += "?, "

    query = query.rstrip(", ") + ");"

    try:
        cur.execute(query, tuple(record.values()))
    except sqlite3.IntegrityError:   # record already exists
        return False

    conn.commit()
    conn.close()


def update(table_name, record: dict, **kwargs):
    """
    Updates a record in the table that has attributes **kwargs, with a new record.
    Returns None if no matching attributes found. 
    """
    pass


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
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    
    if field is None:
        cur.execute(f"SELECT * FROM {table_name}")
        records = cur.fetchall()
        all_records = []
        headers = [column[0] for column in cur.description]

        for record in records:
            all_records.append(dict(zip(headers, record)))

        conn.close()
        return all_records
        
    else:

        try:
            cur.execute(f"SELECT {field} FROM {table_name}")
        except sqlite3.OperationalError:    # field given does not exist
            return None
        else:
            records = cur.fetchall()
            all_records = []

            for record in records:
                for item in record:
                    all_records.append(str(item))

            conn.close()
            return all_records


def find_one(table_name, **kwargs):
    """
    Returns a record with attributes matching **kwargs as a dictionary.
    Returns None f no such record is found. 
    """
    # to fix: does not work for name field only
    conn = sqlite3.connect("test.db")
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


def find_some(table_name, **kwargs):
    """
    Return all records with attributes matching **kwargs as a list of dictionaries.
    Returns None if no such record is found. 
    """
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    output = []

    query = f"SELECT * FROM {table_name} WHERE "
    for key, value in kwargs.items():
        query += f"{key} = {value} AND "

    query = query.rstrip(" AND ") + ";"

    try:
        cur.execute(query)
    except sqlite3.OperationalError:   # record not found
        return None

    records = cur.fetchall()
    headers = [column[0] for column in cur.description]

    for record in records:
        output.append(dict(zip(headers, record)))

    conn.close()
    return output


def find_latest_id(table_name):
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
