from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.name}"

db.create_all()


@app.route('/')
def index():
    return 'Sup!'

@app.route('/api', methods=['POST'])
def create_person():
    data = request.json

    if 'name' not in data or not isinstance(data['name'], str):
        return jsonify({"message": "Invalid input data. 'name' should be a string."}), 400

    person = Person(name=data['name'])
    db.session.add(person)
    db.session.commit()
    return jsonify({"message": "Person created successfully"})

@app.route('/api/<int:user_id>', methods=['GET'])
def get_person_by_id(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404
    return jsonify({"id": person.id, "name": person.name})

@app.route('/api/<int:user_id>', methods=['PUT'])
def update_person(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404
    data = request.json

    
    if 'name' not in data or not isinstance(data['name'], str):
        return jsonify({"message": "Invalid input data. 'name' should be a string."}), 400

    person.name = data['name']
    db.session.commit()
    return jsonify({"message": "Person updated successfully"})

@app.route('/api/<int:user_id>', methods=['DELETE'])
def delete_person(user_id):
    person = Person.query.get(user_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Person deleted successfully"})

@app.route('/api/name/<string:name>', methods=['GET'])
def get_person_by_name(name):
    person = Person.query.filter_by(name=name).first()
    if person is None:
        return jsonify({"message": "Person not found"}), 404
    return jsonify({"id": person.id, "name": person.name})

@app.route('/api', methods=['GET'])
def get_all_people():
    people = Person.query.all()
    people_data = [{"id": person.id, "name": person.name} for person in people]
    return jsonify(people_data)

if __name__ == "__main__":
    app.run(debug=True)
