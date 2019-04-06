import sqlite3
import json
import pickle
from datetime import datetime

def store(method, url, response):
    ''' stores a response in the proxy_database SQLite table'''
    conn = sqlite3.connect('data/proxy_database.db')
    c = conn.cursor()
    # Create table
    init_table(conn, c)
    resp = pickle.dumps(response)
    query = '''REPLACE INTO proxy_responses (method, url, response, timestamp) VALUES (?, ?, ?, ?);'''
    c.execute(query, [method, url, resp, unix_time_millis(datetime.now())])
    conn.commit()
    conn.close()

def retrieve(method, url):
    ''' retrieves a response stored with method and url or None if none is found'''
    conn = sqlite3.connect('data/proxy_database.db')
    c = conn.cursor()
    init_table(conn, c)
    c.execute('SELECT response,timestamp FROM proxy_responses WHERE method = "{mt}" AND url = "{ut}"'
            .format(mt=method, ut=url))
    fetch = c.fetchall()
    conn.close()
    if fetch:
        response = pickle.loads(fetch[0][0])
        timestamp = fetch[0][1]
        return response, timestamp
    else:
        return None, None

def init_table(connection, cursor):
    ''' Initializes SQLite table '''
    if table_exists(cursor):
        return 0
    else:
        cursor.execute('CREATE TABLE {tn} ({f1} {ftt} {nn}, {f2} {ftt} {nn}, {f3} {ftb} {nn}, {f4} {fts} {nn}, PRIMARY KEY({f1},{f2}))'\
        .format(tn="proxy_responses", f1="method", f2="url", f3="response", f4="timestamp", ftt="TEXT", ftb="BLOB", fts="INTEGER", nn="NOT NULL"))
        connection.commit()

def table_exists(cursor):
    ''' Checks if a table exists '''
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='proxy_responses';")
    if cursor.fetchone() == None:
        return False
    else:
        return True

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0
