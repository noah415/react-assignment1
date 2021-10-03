from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from random import seed
from random import randint

seed(6459)
app = Flask(__name__)
CORS(app)

users = { 
   "users_list" :
   [
      { 
         "id" : "xyz789",
         "name" : "Charlie",
         "job": "Janitor",
      },
      {
         "id" : "abc123", 
         "name": "Mac",
         "job": "Bouncer",
      },
      {
         "id" : "ppp222", 
         "name": "Mac",
         "job": "Professor",
      }, 
      {
         "id" : "yat999", 
         "name": "Dee",
         "job": "Aspring actress",
      },
      {
         "id" : "zap555", 
         "name": "Dennis",
         "job": "Bartender",
      }
   ]
}

def add_ID_to_user(user):
   user['id'] = str(randint(0, 10000000000))

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if search_username == user['name']:
               if search_job:
                  if search_job == user['job']:
                     subdict['users_list'].append(user)
               else:
                  subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      add_ID_to_user(userToAdd)
      users['users_list'].append(userToAdd)
      resp = jsonify(userToAdd) #change to jsonify(usertoadd)
      resp.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp
   elif request.method == 'DELETE':
      delete_id = request.args.get('id')
      for i in range(len(users['users_list'])):
         if users['users_list'][i]['id'] == delete_id:
            del users['users_list'][i]
      resp = jsonify(users)
      resp.status_code = 202
      return resp

@app.route('/users/<id>')
def get_user(id):
   if id:
      for user in users['users_list']:
         if user['id'] == id:
           return user
      return ({})
   return users

