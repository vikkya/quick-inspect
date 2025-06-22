import sqlite3

def create_table(db_name, table_name, query):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        create_statment = query
        cur.execute(create_statment)
        conn.commit()
        print("table created")
    except sqlite3.Error as e:
        print(f"someting went wrong {e}")
    finally:
        if conn:
            conn.close()

def delete_all(db_name, table_name):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        create_statment = f"delete from {table_name}"
        cur.execute(create_statment)
        conn.commit()
        print("data cleared")
    except sqlite3.Error as e:
        print(f"someting went wrong {e}")
    finally:
        if conn:
            conn.close()

def drop_table(db_name, table_name):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        drop_statment = f"drop table {table_name}"
        cur.execute(drop_statment)
        conn.commit()
        print("table dropped")
    except sqlite3.Error as e:
        print(f"someting went wrong {e}")
    finally:
        if conn:
            conn.close()

def insert(db_name, table_name):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        insert_statment = f"insert into {table_name} (id) values (1)"
        cur.execute(insert_statment)
        conn.commit()
        print("record inserted")
    except sqlite3.Error as e:
        print(f"someting went wrong {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    db_path = './static/db/qi.db'
    table_name = 'invoice_counter'
    table_name_1 = 'dealers'
    query = f"CREATE TABLE IF NOT EXISTS {table_name} (id integer not null)"
    query_1 = f"CREATE TABLE IF NOT EXISTS {table_name_1} (id integer primary key, name text not null, address text not null, abn text not null)"
    create_table(db_name=db_path, table_name=table_name, query=query)
    create_table(db_name=db_path, table_name=table_name_1, query=query_1)
    # delete_all(db_name=db_path, table_name=table_name)
    # drop_table(db_name=db_path, table_name=table_name)
    insert(db_name=db_path, table_name=table_name)

