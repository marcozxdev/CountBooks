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
        self.danger = False

        for i in value:
            for j in FORBIDDEN_CHARACTERS:
                if i == j:
                    self.danger = True
    
    def insert_data(self, name):
        try:
            self.conn = sql.connect("inventory.db")
            self.cursor = self.conn.cursor()
            self.instruction = f"INSERT INTO inventory VALUES('{name}')"

            self.debug_characters(name)
            
            if self.danger:
                return "Por favor solo ingrese letras y números. No se permiten carácteres especiales."
            else:
                self.cursor.execute(self.instruction) # Critical vulnerability: SQL Inyection
        finally:
            self.conn.commit()
            self.conn.close()
if __name__ == '__main__':
    pass
