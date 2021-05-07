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

  postgreSQL_select_Query= "SELECT pets.id, owners.owner, pets.color, pets.breed, pets.name, pets.checked_in, pets.are_checked_in FROM pets JOIN owners ON owners.id = pets.owner_id;"

  cursor.execute(postgreSQL_select_Query)
  
  pets = cursor.fetchall()
  
  return jsonify(pets)

# def create_owner():

# @app.route('/api/pets', methods=['PUT'] ) 

@app.route('/api/owners', methods=['GET'])
def list_owners():
  cursor = connection.cursor(cursor_factory=RealDictCursor)

  postgreSQL_select_Query= "SELECT COUNT(pets.breed) AS count, owners.owner, owners.id FROM owners LEFT JOIN pets ON owner_id= owners.id GROUP BY owners.id;"
  
  cursor.execute(postgreSQL_select_Query)

  owners = cursor.fetchall()

  return jsonify(owners)

@app.route('/api/pets', methods=['POST'])
def add_pet():
  print('using a multipart form, use request.form:', request.json)
  owner_id = request.json['owner_id']
  breed = request.json['breed']
  color = request.json['color']
  name = request.json['name']
  try:
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    
    print(owner_id, breed, color)
    postgreSQL_select_Query = "INSERT INTO pets (owner_id, breed, color, name) VALUES (%s, %s, %s, %s)"
    
    cursor.execute( postgreSQL_select_Query, (owner_id, breed, color, name,) )
    
    connection.commit()
    count = cursor.rowcount
    print( count, "New Pet added!")
    
    result = { 'status': 'CREATED'}
    return jsonify(result), 201
  except(Exception, psycopg2.Error) as error:
    print('Failed to insert book', error)
    
    result = {'status': 'ERROR'}
    return jsonify(result), 500
  finally:
    
    if(cursor):
      cursor.close()


@app.route('/api/owner', methods=['POST'])
def create_owner():
  print('using multipart from data', request.json)
  owner= request.json['owner']

  try: 
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    print(owner)
    
    postgreSQL_select_Query = "INSERT INTO owners (owner) VALUES (%s);"
    cursor.execute(postgreSQL_select_Query, (owner,))
    connection.commit()
    count=cursor.rowcount
    print(count, "owner inserted")
    result = {'status':'CREATED'}
    return jsonify(result), 201
  except (Exception, psycopg2.Error) as error:
    print("Failed to insert owner")
    result = {'status' : 'ERROR'}
    return jsonify(result), 500
  finally:
    if(cursor):
      cursor.close()


# @app.route("/api/owner/<id>", methods=["DELETE"])
# def delete_owner(id):
#   owner = Owner.query.get(id)
#   db.session.delete(owner)
#   db.session.commit()
  
#   return owner

@app.route('/api/pets/<id>', methods=['DELETE'])
def delete_owner(id):

  # return render_template('data.html')
  print('hello in delete owner:', id)
  ownerID = id
  
  try:
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    print(ownerID)
    
    posgreSQL_deleteOwner_Query = "DELETE FROM pets WHERE id = (%s);"
    cursor.execute(posgreSQL_deleteOwner_Query, (id,))
    connection.commit()
    count = cursor.rowcount
    print(count, 'owner deleted')
    result = {'status':'deleted'}
    return jsonify(result), 201
  except (Exception, psycopg2.Error) as error:
    print('Failed to delete owner', error)
    result = {'status': 'ERROR'}
    return jsonify(result), 500
  finally:
    if(cursor):
      cursor.close()
  
# @app.route('/api/pets', methods=['PUT'])
# def check_in():
#   print('using multipart form in PUT', request.form)
  
#   cursor = connection.cursor(cursor_factory=RealRealDictCursor)
#   postgreSQL_select_Query = "UPDATE pets WHERE owner_id = $1"

app.run()