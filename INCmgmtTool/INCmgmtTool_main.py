from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)

INCIDENTS_FILE = "incidents.json"

# Ensure incidents.json file exists
if not os.path.exists(INCIDENTS_FILE):
    with open(INCIDENTS_FILE, "w") as f:
        json.dump([], f)

def load_incidents():
    with open(INCIDENTS_FILE, "r") as f:
        return json.load(f)

def save_incidents(incidents):
    with open(INCIDENTS_FILE, "w") as f:
        json.dump(incidents, f, indent=4)

@app.route('/')
def index():
    incidents = load_incidents()
    return render_template('index.html', incidents=incidents)

@app.route('/new', methods=['GET', 'POST'])
def new_incident():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        
        new_incident = {
            'id': len(load_incidents()) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'Open',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        incidents = load_incidents()
        incidents.append(new_incident)
        save_incidents(incidents)

        return redirect(url_for('index'))
    return render_template('new_incident.html')

@app.route('/incident/<int:incident_id>')
def view_incident(incident_id):
    incidents = load_incidents()
    incident = next((i for i in incidents if i['id'] == incident_id), None)
    return render_template('view_incident.html', incident=incident)

@app.route('/incident/<int:incident_id>/close')
def close_incident(incident_id):
    incidents = load_incidents()
    for incident in incidents:
        if incident['id'] == incident_id:
            incident['status'] = 'Closed'
            break
    save_incidents(incidents)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
