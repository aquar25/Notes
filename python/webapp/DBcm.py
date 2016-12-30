#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3

# db_config = {
#     'dbname':DB_FILE,
#     'tbname':LOG_TABLE_NAME
#     }

class DataAccessException(Exception):
    pass
        

class UseDatabase(object):
    """docstring for UseDatabase"""
    def __init__(self, config: dict)->None:
        super(UseDatabase, self).__init__()
        self.config = config

    def __enter__(self) -> 'cursor':
        try:
            self.conn = sqlite3.connect(self.config['dbname'])
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as e:
            raise DataAccessException(e)
        

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is sqlite3.OperationalError:
            print('some thing error in with')
            raise DataAccessException('error in exit')
        elif exc_type:
            print('unhandled exceptions', str(type(exc_value)))            
            raise exc_type(exc_value) 
        

if __name__ == '__main__':
    pass


