from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from worker import wrd_counter

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/tasksdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class tasks(db.Model):
    task_id = db.Column(db.String(80), primary_key=True)
    status = db.Column(db.String(80))

    def __init__(self, task_id, status):
        self.task_id = task_id
        self.status = status

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'status': self.status,
        }

@app.route('/count', methods=['POST'])
def count():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify(error="Missing input"), 400
    task = wrd_counter.delay(text)
    task_id = task.id
    response = {'task_id': task_id}
    new = tasks(task_id = task_id, status="Pending")
    db.session.add(new)
    db.session.commit()
    return jsonify(response), 202

@app.route('/status/<string:task_id>', methods=['GET'])
def status(task_id):
    task = tasks.query.get(task_id)
    if not task:
        return jsonify({'status': 'not found'}), 404

    result = wrd_counter.AsyncResult(task_id)
    if result.state == "Success":
        task.status = "Success"
        db.session.commit()
        return jsonify({'result': result.get(), 'status': 'completed'}), 200
    else:
        task.status = result.state
        db.session.commit()
        return jsonify({'status': result.state}), 202

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 5050)