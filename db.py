import sqlite3


def init_db(force: bool = False):
    with sqlite3.connect('SparkRead.db') as conn:
        c = conn.cursor()

        if force:
            c.execute('DROP TABLE IF EXISTS SparkRead;')

        c.execute('''
                CREATE TABLE IF NOT EXISTS SparkRead (
                user_id     STRING NOT NULL,
                book_1      STRING NOT NULL,
                book_2      STRING NOT NULL,
                book_3      STRING NOT NULL);
            ''')

        conn.commit()


def add_user(user_id: str, book_1: str, book_2: str, book_3: str):
    with sqlite3.connect('SparkRead.db') as conn:
        c = conn.cursor()
        s = '''INSERT INTO SparkRead VALUES ('{}', '{}', '{}', '{}');'''.\
            format(user_id, book_1, book_2, book_3)
        try:
            c.execute(s)
        except Exception as e:
            print(e)

        conn.commit()

