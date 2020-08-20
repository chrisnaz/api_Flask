from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Person Class/Model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name
# Person Schema
class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id','name')

# Init schema
person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)

# Create a Person
@app.route('/person', methods=['POST'])
def add_person():
    name = request.json['name']

    new_person = Person(name)

    db.session.add(new_person)
    db.session.commit()

    return person_schema.jsonify(new_person)

# Get all Person
@app.route('/person', methods=['GET'])
def get_persons():
    all_persons = Person.query.all()
    result = persons_schema.dump(all_persons)
    return jsonify(result)

# Get Single Person
@app.route('/person/<id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    return person_schema.jsonify(person)

# Update a Person
@app.route('/person/<id>', methods=['PUT'])
def update_person(id):
    person = Person.query.get(id)
    
    name = request.json['name']

    person.name = name

    db.session.commit()

    return person_schema.jsonify(person)

# Delete Person
@app.route('/person/<id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()
    return person_schema.jsonify(person)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)