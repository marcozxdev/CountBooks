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

    def debug_characters(self, value):
        FORBIDDEN_CHARACTERS = ["-", ";", "_", "(", ")", "+", "'"]

        for i in value:
            if i == FORBIDDEN_CHARACTERS:
                pass
    
    def insert_data(self):
        try:
            self.conn = sql.connect("inventory.db")
            self.cursor = self.conn.cursor()
            self.instruction = f"INSERT INTO inventory VALUES('{name}')"
          
            self.cursor.execute(self.instruction) # Critical vulnerability: SQL Inyection
        finally:
            self.conn.commit()
            self.conn.close()
if __name__ == '__main__':
    pass
