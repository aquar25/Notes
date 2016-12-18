#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, escape

app = Flask(__name__)

LOG_FILE = 'req_log.txt'

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
    log_req(request)
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

def log_req(req:'flask_request') -> None:
    with open(LOG_FILE, 'a') as logfile:
        print(req.form, req.remote_addr, req.user_agent, file=logfile, sep='|')

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

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)


