import sqlite3
import json
import pickle

def store(method, url, response):
    ''' stores a response in the proxy_database SQLite table'''
    conn = sqlite3.connect('data/proxy_database.db')
    c = conn.cursor()
    # Create table
    init_table(conn, c)
    resp = pickle.dumps(response)
    query = '''INSERT INTO proxy_responses (method, url, response) VALUES (?, ?, ?);'''
    c.execute(query, [method, url, resp])
    conn.commit()
    conn.close()

def retrieve(method, url):
    ''' retrieves a response stored with method and url or None if none is found'''
    conn = sqlite3.connect('data/proxy_database.db')
    c = conn.cursor()
    init_table(conn, c)
    c.execute('SELECT response FROM proxy_responses WHERE method = "{mt}" AND url = "{ut}"'
            .format(mt=method, ut=url))
    response = c.fetchone()
    conn.close()
    if response != None:
        response = pickle.loads(response[0])
    return response

def init_table(connection, cursor):
    ''' Initializes SQLite table '''
    if table_exists(cursor):
        return 0
    else:
        cursor.execute('CREATE TABLE {tn} ({f1} {ftt} {nn}, {f2} {ftt} {nn}, {f3} {ftb} {nn}, PRIMARY KEY({f1},{f2}))'\
        .format(tn="proxy_responses", f1="method", f2="url", f3="response", ftt="TEXT", ftb="BLOB", nn="NOT NULL"))
        connection.commit()

def table_exists(cursor):
    ''' Checks if a table exists '''
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='proxy_responses';")
    if cursor.fetchone() == None:
        return False
    else:
        return True
