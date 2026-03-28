from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
DATA_FILE = 'pomodoro_data.json'
TAGS_FILE = 'pomodoro_tags.json'
PHRASES_FILE = 'frases_personalizadas.txt'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'history': []}


def load_tags():
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    tags = ['Análisis', 'TFG']
    with open(TAGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False)
    return tags


def save_tags(tags):
    with open(TAGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


@app.route('/')
def index():
    data = load_data()
    tags = load_tags()
    today = datetime.now().strftime('%Y-%m-%d')
    calendar = {}
    for entry in data['history']:
        date = entry['datetime'].split()[0]
        calendar[date] = calendar.get(date, 0) + 1
    pomodoros_today = calendar.get(today, 0)
    return render_template('index.html', pomodoros_today=pomodoros_today,
                           calendar=calendar, history=data['history'], tags=tags)


@app.route('/add_pomodoro', methods=['POST'])
def add_pomodoro():
    data = load_data()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    duration = request.json.get('duration', 25)
    tag = request.json.get('tag', '')
    productivity = request.json.get('productivity', 0)  # 0-5 stars
    data['history'].append({
        'datetime': now,
        'duration': duration,
        'tag': tag,
        'productivity': productivity
    })
    save_data(data)
    return jsonify({'success': True})


@app.route('/get_tags')
def get_tags():
    tags = load_tags()
    return jsonify({'tags': tags})


@app.route('/add_tag', methods=['POST'])
def add_tag():
    tags = load_tags()
    new_tag = request.json.get('tag', '').strip()
    if new_tag and new_tag not in tags:
        tags.append(new_tag)
        save_tags(tags)
        return jsonify({'success': True, 'tags': tags})
    return jsonify({'success': False, 'tags': tags})


@app.route('/delete_tag', methods=['POST'])
def delete_tag():
    tags = load_tags()
    tag_to_delete = request.json.get('tag', '').strip()
    if tag_to_delete in tags:
        tags.remove(tag_to_delete)
        save_tags(tags)
        return jsonify({'success': True, 'tags': tags})
    return jsonify({'success': False, 'tags': tags})


def load_phrases():
    """Returns list of phrases from frases_personalizadas.txt, or None if the file doesn't exist."""
    if os.path.exists(PHRASES_FILE):
        with open(PHRASES_FILE, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
        return lines if lines else None
    return None


@app.route('/get_phrases')
def get_phrases():
    phrases = load_phrases()
    return jsonify({'phrases': phrases})


@app.route('/get_data')
def get_data():
    data = load_data()
    today = datetime.now().strftime('%Y-%m-%d')
    calendar = {}
    for entry in data['history']:
        date = entry['datetime'].split()[0]
        calendar[date] = calendar.get(date, 0) + 1
    pomodoros_today = calendar.get(today, 0)
    return jsonify({
        'pomodoros_today': pomodoros_today,
        'calendar': calendar,
        'history': data['history']
    })


@app.route('/get_day/<date>')
def get_day(date):
    data = load_data()
    pomodoros = [e for e in data['history'] if e['datetime'].startswith(date)]
    return jsonify({'pomodoros': pomodoros})


@app.route('/weekly_report')
def weekly_report():
    data = load_data()
    today = datetime.now().date()
    # Start of week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    report = {}  # tag -> total minutes
    total_sessions = 0
    total_productivity = 0
    productivity_count = 0

    for entry in data['history']:
        entry_date = datetime.strptime(entry['datetime'], '%Y-%m-%d %H:%M:%S').date()
        if start_of_week <= entry_date <= end_of_week:
            tag = entry.get('tag', 'Sin etiqueta') or 'Sin etiqueta'
            duration = entry.get('duration', 25)
            report[tag] = report.get(tag, 0) + duration
            total_sessions += 1
            prod = entry.get('productivity', 0)
            if prod > 0:
                total_productivity += prod
                productivity_count += 1

    avg_productivity = round(total_productivity / productivity_count, 1) if productivity_count > 0 else 0

    # Convert minutes to hours + minutes
    report_formatted = {}
    for tag, mins in report.items():
        h = mins // 60
        m = mins % 60
        report_formatted[tag] = {'minutes': mins, 'display': f'{h}h {m}min' if h > 0 else f'{m}min'}

    return jsonify({
        'week_start': str(start_of_week),
        'week_end': str(end_of_week),
        'report': report_formatted,
        'total_sessions': total_sessions,
        'avg_productivity': avg_productivity
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
