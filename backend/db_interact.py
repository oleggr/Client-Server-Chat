import os
import sqlite3
import db_queries as db_q


db_filename = 'sqlite.db'


def db_initialization():

    try:
        sqliteConnection = sqlite3.connect(db_filename)
        
        cursor = sqliteConnection.cursor()
        cursor.execute(db_q.sqlite_create_messages_table_query)
        cursor.execute(db_q.sqlite_create_users_table_query)
        cursor.execute(db_q.sqlite_create_chats_table_query)

        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()

        return 'OK'

    except sqlite3.Error as error:
        return 'Error while connecting to database {}'.format(error)


def db_drop():

    try:
        os.remove(db_filename)
        return 'DB was deleted'

    except Exception as e:
        return "Error while deleting db {}".format(e)


def send_message(message):

    try:
        sqliteConnection = sqlite3.connect(db_filename)

        cursor = sqliteConnection.cursor()
        cursor.execute(message.set_message_sql_query, (message.sender, message.receiver, message.text, message.created_at))

        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()

        reply = {'sender': message.sender,
                'receiver': message.receiver,
                'text': message.text,
                'created_at': message.created_at}

        return reply

    except Exception as e:
        return "Error while sending message {}".format(e)


def receive_messages(username):

    try:
        sqliteConnection = sqlite3.connect(db_filename)

        cur = sqliteConnection.cursor()
        cur.execute('SELECT * FROM messages WHERE receiver=\'{}\' and is_checked=\'{}\''.format(username, False))
     
        rows = cur.fetchall()
        res = []
     
        for row in rows:
            res.append(row)

        sqliteConnection.close()

        return res

    except Exception as e:
        return "Error while getting messages {}".format(e)


def select_all_messages():

    try:
        sqliteConnection = sqlite3.connect(db_filename)

        cur = sqliteConnection.cursor()
        cur.execute(db_q.select_all_messages)
     
        rows = cur.fetchall()
        res = []
     
        for row in rows:
            res.append(row)

        sqliteConnection.close()

        return res

    except Exception as e:
        return "Error while getting messages {}".format(e)


def drop_all_messages():

    try:
        sqliteConnection = sqlite3.connect(db_filename)

        cursor = sqliteConnection.cursor()
        cursor.execute(db_q.delete_all_messages)
     
        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()

        return 'All messages was deleted'

    except Exception as e:
        return "Error while deleting messages {}".format(e)


def user_create(user):

    try:
        sqliteConnection = sqlite3.connect(db_filename)

        if user_exist(user.username):
            return 'User exist. Try another username.'

        cursor = sqliteConnection.cursor()
        cursor.execute(user.set_user_sql_query, (user.username, user.password_hash, user.created_at))

        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()

        reply = {'username': user.username,
                'created_at': user.created_at}

        return reply

    except Exception as e:
        return "Error while creating user {}".format(e)


def user_login(username, password_hash):

    try:
        sqliteConnection = sqlite3.connect(db_filename)

        cursor = sqliteConnection.cursor()
        cursor.execute('SELECT username FROM users WHERE username=\'{}\' and password_hash=\'{}\''.format(username, password_hash))

        rows = cursor.fetchall()
        print(rows)

        sqliteConnection.commit()

        if len(rows) > 0:

            cursor.execute('SELECT id FROM users WHERE username=\'{}\' and password_hash=\'{}\''.format(username, password_hash))
            user_id = cursor.fetchall()

            cursor.close()
            sqliteConnection.close()

            return str(user_id[0][0])

        else:
            cursor.close()
            sqliteConnection.close()
            return 'Incorrect data.'


    except Exception as e:
        return "Error while login user {}".format(e)


def user_exist(username):
    try:
        sqliteConnection = sqlite3.connect(db_filename)

        cursor = sqliteConnection.cursor()
        cursor.execute('SELECT username FROM users WHERE username=\'{}\''.format(username))

        rows = cursor.fetchall()

        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()

        if len(rows) != 0:
            return True
        else:
            return False

    except Exception as e:
        return "Error while checking username {}".format(e)


def select_all_users():

    try:
        sqliteConnection = sqlite3.connect(db_filename)

        cur = sqliteConnection.cursor()
        cur.execute(db_q.select_all_users)
     
        rows = cur.fetchall()
        res = []
     
        for row in rows:
            res.append(row)

        sqliteConnection.close()

        return res

    except Exception as e:
        return "Error while getting users {}".format(e)


def db_test_data_load():
    pass
