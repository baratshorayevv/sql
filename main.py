import sqlite3
from contextlib import contextmanager

@contextmanager
def db_connection(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

class Book:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with db_connection(self.db_name) as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                author TEXT NOT NULL,
                                year INTEGER NOT NULL
                            )''')

    def create(self, title, author, year):
        with db_connection(self.db_name) as cursor:
            cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))

    def read(self, book_id):
        with db_connection(self.db_name) as cursor:
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            return cursor.fetchone()

    def update(self, book_id, title, author, year):
        with db_connection(self.db_name) as cursor:
            cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", (title, author, year, book_id))

    def delete(self, book_id):
        with db_connection(self.db_name) as cursor:
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))

db_name = 'books.db'
book = Book(db_name)

book.create('Book Title 1', 'Author 1', 2021)

print(book.read(1))

book.update(1, 'Updated Title', 'Updated Author', 2022)

book.delete(1)

import sqlite3

def view_books(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows

db_name = 'books.db'
books = view_books(db_name)
for book in books:
    print(book)
import psycopg2

def view_books(db_name, user, password, host, port):
    conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows

db_name = 'n48'
user = 'postgres'
password = '123'
host = 'localhost'
port = '5432'

books = view_books(db_name, user, password, host, port)
for book in books:
    print(book)

