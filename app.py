from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    # Increase the counter on each visit
    with app.app_context():
        visit = Visit()
        db.session.add(visit)
        db.session.commit()

    # Get data for the histogram
    with app.app_context():
        visits = Visit.query.all()
        timestamps = [visit.timestamp.strftime('%Y-%m-%d %H:%M:%S') for visit in visits]

    return render_template('index.html', timestamps=timestamps)

@app.route('/data')
def data():
    # Get data for the histogram in JSON format
    with app.app_context():
        visits = Visit.query.all()
        timestamps = [visit.timestamp.strftime('%Y-%m-%d %H:%M:%S') for visit in visits]

    return jsonify({'timestamps': timestamps})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
