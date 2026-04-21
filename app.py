import sqlite3 as sql

class DataBase:
    def __init__(self):
        self.conn = sql.connect("inventory.db")
        self.conn.commit()
        self.conn.close()

        self.create_table()

    def create_table(self):
        try:
            self.conn = sql.connect("inventory.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute(
              """CREATE TABLE IF NOT EXISTS inventory(
                    name TEXT,
                    last_name TEXT,
                    age INTEGER
              )"""
            )
        finally:
            self.conn.commit()
            self.conn.close()

    def insert_data(self):
        try:
            self.conn = sql.connect("inventory.db")
            self.cursor = self.conn.cursor()
            self.instruction = f"INSERT INTO inventory VALUES('{name}')"ñ
          
            self.cursor.execute()

if __name__ == '__main__':
    pass
