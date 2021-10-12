"""
Noah Otsuka
CSC307

$ export FLASK_APP=sample_backend.py
$ export FLASK_ENV=development
$ flask run
"""

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from random import seed
from random import randint
import model_mongodb as db

seed(6459)
app = Flask(__name__)
CORS(app)

# implementing the mongodb
db_users = db.User()

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username:
         if search_job:
            ret = jsonify(db_users.find_by_name_job(search_username, search_job))
         else:
            ret = jsonify(db_users.find_by_name(search_username))

         return ret
      ret = jsonify(db_users.find_all())
      return ret
   elif request.method == 'POST':
      userToAdd = request.get_json()
      # add logic here
      new_user = db.Model()
      new_user['name'] = userToAdd['name']
      new_user['job'] = userToAdd['job']
      new_user.save()
      ret = jsonify(db_users.find_by_id(new_user['_id'])[0])
      ret.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return ret
   elif request.method == 'DELETE':
      delete_id = request.args.get('id')

      old_user = db.Model()
      old_user["_id"] = delete_id
      if old_user.remove():
         resp = jsonify(success=True)
         resp.status_code = 204
      else:
         resp = jsonify(success=False)
         resp.status_code = 404

      return resp

@app.route('/users/<id>')
def get_user(id):
   if id:
      return jsonify(db_users.find_by_id(id))
   return jsonify(db_users.find_all())

