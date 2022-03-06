import sqlite3
from quote_book.config import paths

quote_db = sqlite3.connect(paths['data'], check_same_thread=False)

user_db = sqlite3.connect(paths['users'], check_same_thread=False)