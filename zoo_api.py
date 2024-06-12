import flask
from flask import jsonify
from flask import request

from sql import create_connection
from sql import execute_query
from sql import execute_read_query

from random import randrange


class Creds:
    host = 'host'
    user = 'user'
    password = 'password'
    database = 'database'


app = flask.Flask(__name__)
app.config["DEBUG"] = True

conn = create_connection(Creds.host, Creds.user, Creds.password, Creds.database)


# return all animals from zoo
@app.route('/api/zoo/all', methods=['GET'])
def all_animals():
    sql = "SELECT * FROM zoo"
    zoo = execute_read_query(conn, sql)
    return jsonify(zoo)


# add new animal to zoo //added auto create id (range of 2 digits to 3 digits)
@app.route('/api/zoo', methods=['POST'])
def new_animal():
    request_data = request.get_json()
    nid = randrange(10, 1000)
    ndomain = request_data['domain']
    nkingdom = request_data['kingdom']
    nclass = request_data['class']
    nspecies = request_data['species']
    nage = request_data['age']
    nanimalname = request_data['animalname']
    nalive = request_data['alive']

    sql = "INSERT INTO zoo(id, domain, kingdom, class, species, age, animalname, alive) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (nid, ndomain, nkingdom, nclass,
                                                                       nspecies, nage, nanimalname, nalive)
    execute_query(conn, sql)

    return 'add successful'


# update column of animal provided id
@app.route('/api/zoo', methods=['PUT'])
def update_active():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No ID is provided!'
    sql = "SELECT * FROM zoo"
    request_data = request.get_json()
    nalive = request_data['alive']
    animls = execute_read_query(conn, sql)
    sqll = "UPDATE zoo SET alive = %s WHERE id = %s" % (nalive, id)
    for anim in animls:
        if anim['id'] == id:
            execute_query(conn, sqll)

    return 'update successful'


# delete animal provided id
@app.route('/api/zoo', methods=['DELETE'])
def del_animal():
    request_data = request.get_json()
    idtodelete = request_data['id']

    sql = "DELETE FROM zoo WHERE id = %s" % idtodelete
    execute_query(conn, sql)

    return 'delete successful'


app.run()
