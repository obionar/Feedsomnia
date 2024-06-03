#!/usr/bin/env python3

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Convert timestamps to human-readable format
def datetimeformat(value):
    try:
        timestamp = int(float(value))
        formatted_date = datetime.fromtimestamp(timestamp).strftime("%d/%m %H:%M")
        return formatted_date
    except ValueError:
        return value

# Register the filter for Jinja2
app.jinja_env.filters['datetimeformat'] = datetimeformat

def get_countries():
    try:
        con = sqlite3.connect('../feeds.db')
        cur = con.cursor()
        cur.execute('SELECT DISTINCT Country FROM Feeds')
        countries = [row[0] for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        countries = []
    finally:
        if con:
            con.close()
    return countries

@app.route('/', methods=['GET'])
def main():
    countries = get_countries()
    return render_template('main.html', countries=countries)

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('kw')
    country = request.args.get('country')
    query = '1=1'

    if keyword:
        for word in keyword.split():
            word = word.replace('+', ' ')
            if '<' in word:
                query += f' AND Price < ?'
            elif '>' in word:
                query += f' AND Price > ?'
            else:
                query += f' AND Description LIKE ?'
    
    if country and country != 'All Countries':
        query += f' AND Country = ?'

    params = []
    if keyword:
        for word in keyword.split():
            if '<' in word or '>' in word:
                params.append(word.replace('<', '').replace('>', ''))
            else:
                params.append(f"%{word}%")
    if country and country != 'All Countries':
        params.append(country)

    print(f"Constructed Query: {query}")

    try:
        con = sqlite3.connect('../feeds.db')
        cur = con.cursor()
        cur.execute(f'''SELECT URL, Title, Price, Date, Country, Sitename 
                        FROM Feeds 
                        WHERE {query} 
                        ORDER BY id DESC 
                        LIMIT 100''', params)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        rows = []
    finally:
        if con:
            con.close()

    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
