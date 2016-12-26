#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3

# db_config = {
#     'dbname':DB_FILE,
#     'tbname':LOG_TABLE_NAME
#     }

class UseDatabase(object):
    """docstring for UseDatabase"""
    def __init__(self, config: dict)->None:
        super(UseDatabase, self).__init__()
        self.config = config

    def __enter__(self) -> 'cursor':
        self.conn = sqlite3.connect(self.config['dbname'])
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        

if __name__ == '__main__':
    pass


