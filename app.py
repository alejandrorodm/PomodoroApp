from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = 'pomodoro_data.json'

# Utilidades para guardar y cargar datos

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'history': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    data = load_data()
    today = datetime.now().strftime('%Y-%m-%d')
    calendar = {}
    for entry in data['history']:
        date = entry.split()[0]
        calendar[date] = calendar.get(date, 0) + 1
    pomodoros_today = calendar.get(today, 0)
    return render_template('index.html', pomodoros_today=pomodoros_today, calendar=calendar, history=data['history'])

@app.route('/add_pomodoro', methods=['POST'])
def add_pomodoro():
    data = load_data()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['history'].append(now)
    save_data(data)
    return jsonify({'success': True})

@app.route('/get_data')
def get_data():
    data = load_data()
    today = datetime.now().strftime('%Y-%m-%d')
    calendar = {}
    for entry in data['history']:
        date = entry.split()[0]
        calendar[date] = calendar.get(date, 0) + 1
    pomodoros_today = calendar.get(today, 0)
    return jsonify({'pomodoros_today': pomodoros_today, 'calendar': calendar, 'history': data['history']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
