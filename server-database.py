import flask
import psycopg2
from flask import request, jsonify
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"] = True

connection = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="pet_hotel"
)

@app.route('/', methods=['GET'])
def home():
  return "<h1>Home Pet Hotel Page</h1>"

@app.route('/api/pets', methods=['GET'])
def list_pets():
  cursor = connection.cursor(cursor_factory=RealDictCursor)

  postgreSQL_select_Query= "SELECT * FROM pets JOIN owners ON owners.id = pets.owner_id;" 

  cursor.execute(postgreSQL_select_Query)
  
  pets = cursor.fetchall()
  
  return jsonify(pets)
# @app.route('/api/pets', methods=['POST'])
# def create_owner():

# @app.route('/api/pets', methods=['PUT'] ) 


app.run()