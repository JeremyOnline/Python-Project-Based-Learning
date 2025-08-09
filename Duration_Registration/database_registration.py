import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        # Membuat tabel jika belum ada
        pass
    
    def execute_query(self, query, params=None):
        # Fungsi untuk eksekusi query
        pass
