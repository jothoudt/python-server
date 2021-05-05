import flask
import pyscopg2
from flask import request, jsonify
from psycopg2.extras import RealDictCursor

app= flask.Flask(__name__)
app.config["DEBUG"] = True

connection = pyscopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="pet_hotel"
)

@app.route('/api/pets', methods=['GET'])
  def list_pets():