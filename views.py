from sensorsapi import app
from models import *
from flask import jsonify, request, render_template


@app.route('/', methods=['GET'])
def index():
    last_entries = SensorsEntry.query.order_by(SensorsEntry.timestamp.desc()).limit(10)
    all_entries = SensorsEntry.query.all()
    return render_template('index.html', last_entries=last_entries, all_entries=all_entries)


@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = []
    for entry in SensorsEntry.query.all():
        entries.append(entry.export_data())

    return jsonify({'entries': entries})


@app.route('/api/entries/<id>', methods=['GET'])
def get_entry(id):
    return jsonify(SensorsEntry.query.get_or_404(id).export_data())


@app.route('/api/entries', methods=['POST'])
def post_entry():
    entry = SensorsEntry()
    entry.import_data(request.json)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.export_data()), 201
