import sqlite3

__connection = None


def get_connection():  #Get connection with database
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('botdata.db', check_same_thread=False)
    return __connection


def init_db(force: bool = False):

    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS olimob_apps')

    c.execute('''
        CREATE TABLE IF NOT EXISTS olimob_apps (
            id              INTEGER PRIMARY KEY, 
            url             INTEGER UNIQUE, 
            name            TEXT,
            flag            INTEGER default 0)
            ''')
    conn.commit()


def add_user(user_id: int):  # Add user id into database
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO olimob_users (user_id) VALUES (?)',
                 (user_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        print('User already exists')


def add_app_name(name: str):  # Add app_name to database
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO olimob_apps (user_id) VALUES (?)',
                 (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print('User already exists')


def add_app_desc(url: str, name: str):  # Add app URL into database
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO olimob_apps (url, name) VALUES (?, ?)',
                 (url, name, ))
        conn.commit()
    except sqlite3.IntegrityError:
        print('App already exists')


def subscribe(subscription: int, user_id: int):    # Subscribe to mailing. Only 2 values: 0 or 1, if 1 = True
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE olimob_users SET subscription = ? WHERE user_id = ?',
             (subscription, user_id))
    conn.commit()


def admin_check(user_id: int):   # User role checking
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT role FROM olimob_users WHERE user_id = ?',
             (user_id, ))
    conn.commit()
    role_type = c.fetchone()
    for row in role_type:
        return row


def get_subscribed_users():   # User role checking
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT user_id FROM olimob_users WHERE subscription = 1')
    conn.commit()
    return c.fetchall()



def get_random_message(): #Getting random message for users
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT text FROM user_message ORDER BY RANDOM() LIMIT 1',)
    return c.fetchall()


def get_user_message(user_id: int, limit: int = 2): #Getting list of user messages
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT text FROM user_message WHERE user_id = ? ORDER BY id LIMIT ?', (user_id, limit))
    return c.fetchall()


def get_app_link():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT url FROM olimob_apps ORDER BY id',)
    return c.fetchall()


def change_flag(url: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE olimob_apps SET flag = 1 WHERE url = ?', (url, ))
    conn.commit()


def get_app_status():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT url FROM olimob_apps WHERE flag = 1 ', )
    a = c.fetchone()
    try:
        for i in a:
            return i
    except TypeError:
        return c.fetchone()


def get_app_name():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT name FROM olimob_apps WHERE flag = 1 ', )
    get_only_app_name = c.fetchone()
    for i in get_only_app_name:
        return i


def delete_app(url: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM olimob_apps WHERE url = ? ', (url, ))
    conn.commit()
