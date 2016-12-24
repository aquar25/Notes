#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, escape
import sqlite3

app = Flask(__name__)

LOG_FILE = 'req_log.txt'
DB_FILE = 'log.db'
LOG_TABLE_NAME = 'req_log'

LOG_TYPE_TXT = 'TXT'
LOG_TYPE_DB = 'SQL'


@app.route('/')
def home() ->'302':
    # redirect to the future page
    return redirect('/future')

@app.route('/f')
@app.route('/future') # GET method by default
def future_page():
    return render_template('future.html', the_title='Forsee the Future')

@app.route('/calc', methods=['POST']) # supports only the POST method
def calc_page() ->'html':
    month = int(request.form['month'])
    day = int(request.form['day'])
    result = get_constellation(month, day)
    log_req(request, LOG_TYPE_DB)
    return render_template('result.html', the_title='Your Future is here', result=result)

@app.route('/reqlog')
def show_log():
    contents = []
    with open(LOG_FILE) as logfile:
        for line in logfile:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote Addr', 'User Agent')
    return render_template('reqlog.html',
                            the_title = 'View Logs',
                            the_row_titles=titles,
                            the_data=contents,)

def log_req(req:'flask_request', log_type:str=LOG_TYPE_TXT) -> None:
    if log_type == LOG_TYPE_TXT:
        with open(LOG_FILE, 'a') as logfile:
            print(req.form, req.remote_addr, req.user_agent, file=logfile, sep='|')
    else:
        add_log_db(req.form['year'], req.form['month'], req.form['day'], 
            req.remote_addr, req.user_agent.browser)



def letter_in_phrase(phrase: str, letters: str='aeiou') -> set:
    """Get the letters in the phrase"""
    return set(letters).intersection(set(phrase))

def get_constellation(month, day):
    days = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
    constellations = ('Capricorn', 'Aquarius', 'Pisces', 'Aries', 
        'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 
        'Scorpio', 'Sagittarius','Capricorn')
    if day < days[month-1]:
        return constellations[month-1]
    else:
        return constellations[month]

def init_database():
    createtable = """create table req_log
          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          year varchar(10),
          month varchar(10),
          day varchar(10),
          address varchar(25),
          browser varchar(50))"""
    # connect to the database, if file is not exist, this will create it 
    conn = sqlite3.connect(DB_FILE)
    # create a Cursor
    cursor = conn.cursor()
    showtables = """select name from sqlite_master where type='table' order by name"""
    cursor.execute(showtables)
    result = cursor.fetchall()
    if len(result) == 0:
         # execute a sql statement
         cursor.execute(createtable)
    else:
        print(result)    
    
    # close the Cursor
    cursor.close()
    # commit the transaction
    conn.commit()
    # close the connect
    conn.close()

def add_log_db(year, month, day, address, browser):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    _sql = "insert into "  + LOG_TABLE_NAME + " (year, month, day, address, browser) values "
    values = "(" + year + "," + month + "," + day + ", '" + str(address) + "','"+ browser +"')"         
    print(_sql+values)
    cursor.execute(_sql+values)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_database()
    app.run('0.0.0.0', debug=True)


