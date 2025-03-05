import psycopg2
from psycopg2.extensions import register_adapter, AsIs

import numpy as np

from .config import DatabaseConfig

register_adapter(np.int64, AsIs)

class Database:
    def __init__(self, config):
        self.conn = None
        self.config = config

    def connect(self):
        params = self.config
        self.conn = psycopg2.connect(**params)
        return self.conn

    def create_table(self, table_file):
        cursor = self.conn.cursor()
        cursor.execute(open(table_file, 'r').read())
        self.conn.commit()

    def get_data(self, select_query):
        cursor = self.conn.cursor()
        cursor.execute(select_query)
        select_data = cursor.fetchall()
        return select_data

    def insert_data(self, insert_query, data):
        cursor = self.conn.cursor()
        cursor.execute(insert_query, data)
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    postgres_config_params = DatabaseConfig(filename = 'db/database.ini', section = 'postgresql').get_config_params()
    db = Database(postgres_config_params)
    db.connect()
    db.close()