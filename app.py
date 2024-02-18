import sqlite3
import os
import dateutil.parser

def get_connection_and_cursor(db_file: str) -> (sqlite3.Connection, sqlite3.Cursor):
    """
    Returns cursor and connection to database file.
    """
    conn = sqlite3.connect(database=db_file)

    cursor = conn.cursor()

    return conn, cursor

def init_db(db_file: str) -> (sqlite3.Connection, sqlite3.Cursor):
    """
    Initializes database at file path `db_file`. Returns cursor and connection to database file.
    """
    conn, cursor = get_connection_and_cursor(db_file)

    cursor.execute("DROP TABLE IF EXISTS employees")

    conn.commit()

    cursor.execute("""
CREATE TABLE employees 
                        (employee_id integer PRIMARY KEY, 
                        employee_email TEXT,
                        last_status_change TIMESTAMP WITH TIME ZONE,
                        status TEXT)
                   """)
    
    conn.commit()

    values = [
        (1, 'jim_d_smith@company.com', dateutil.parser.parse('2022-02-03'), 'part-time'),
        (2, 'jill_jones@company.com', dateutil.parser.parse('2023-03-03'), 'full-time'),
        (3, 'raul_garcia@company.com', dateutil.parser.parse('2021-04-03'), 'resigned'),
        (4, 'tom_cruise@company.com', dateutil.parser.parse('2022-05-03'), 'terminated')
    ]

    for emp_id, emp_email, status_change, status in values:
        cursor.execute("insert into employees (employee_id, employee_email, last_status_change, status) values (?, ?, ?, ?)", (emp_id, emp_email, status_change, status))

    conn.commit()

    return conn, cursor

def view_records(cursor, emp_ids):
    statements_str = ""

    for emp_id in emp_ids.split(","):
        statements_str += f"select * from employees where employee_id = {emp_id};"

    print(statements_str)

    results = list()

    for statement in statements_str.split(';'):
        result = cursor.execute(statement)

        results.extend([row for row in result.fetchall()])

    return results

def display_all_info(cursor):
    results = cursor.execute("select * from employees")

    return [row for row in results.fetchall()]

def main():
    db_file = 'mydb.sqlite3'

    conn, cursor = init_db(db_file)

    print("Welcome to employee HR system. Please enter employee id to view data on a specific employee. If you want to see all employee data, enter 'ALL'. You can enter several employee ids, separated by commas, if you want to view several employees. Example: 1,2,3.\n\n")
    
    while True:
        try:
            id_or_all = input('Employee id or "ALL": ').strip()

            if id_or_all == "ALL":
                print(display_all_info(cursor))
            else:
                print(view_records(cursor, id_or_all))
        except KeyboardInterrupt:
            print("Exiting program due to Ctrl-C.")

            if cursor:
                cursor.close()

            if conn:
                conn.close()

            break

if __name__ == "__main__":
    main()
