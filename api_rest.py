
#Premiere version du backend python Verbose.
#Un petit Mitsubishi
from flask import Flask
from flask_restful import Resource, Api
from flask import request
from datetime import datetime
import json
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

mode="mongodb+srv://verbose:verbose@cluster0.4s7fd.mongodb.net/pydb?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
try:
	db=PyMongo(app, uri=mode).db	
except:
	pass
@app.route('/ping')
def db_v():
	try:
		db=PyMongo(app, uri=mode).db
		return {'status':'success', 'data': 'pong'}
	except:
		return {'status':'error', 'data': 'plouff'}
	

@app.route("/todo")
#Fonction de recupération de tous les Todos
def get():
	todos=db.TODO.find()
	TODO_list=[]
	for todo in todos:
		todo["_id"]=str(todo["_id"])
		TODO_list.append(todo)
	return {'status':'success', 'data': TODO_list}


@app.route("/todo/<id>")
#Fonction pour recupérer un Todos en particulier
def get_id(id):
	todo=db.TODO.find_one({"_id":ObjectId(id)})
	if todo is None:
		return {'status':'error', 'data': "Identifiant n'existe pas"}
	todo["_id"]=str(todo["_id"])
	return {'status':'success', 'data': todo }


@app.route( '/todo', methods=['POST'])
#Fonction pour créer un Todos
def ajouter_tache():
	try:
		temps= str(datetime.now())
		todo={'label':request.json['label'], 'createdAt':temps, 'updatedAt':temps}
		db.TODO.insert_one(todo)
		todo["_id"]=str(todo["_id"])
		return {'status': 'success', 'data':todo}
	except:
		return {'status':'error', 'data': "une erreur dans l'execution "}


@app.route('/todo/<id>', methods=['DELETE'])
def supprimer(id):
	todo=db.TODO.find_one({"_id":ObjectId(id)})
	db.TODO.remove(todo)
	if todo is None:
		return {"status":"error", 'data':"Identifiant n'existe pas"}
	return {'status':'success', 'data':'task deleted'}


@app.route('/todo/<id>', methods=['PUT'])
#Fonction pour modifier un Todos
def update(id):
	todo=db.TODO.find_one({"_id":ObjectId(id)})
	if todo is None:
		return {'status':'error', 'description':'tache non retrouvée'}
	temps= str(datetime.now())
	todo["label"]=request.json['label']
	#todo.label= todos.label
	todo["updatedAt"]= temps
	todo["_id"]=str(todo["_id"])
	return {'status':'sucess','data':todo}


if __name__ == '__main__':
    app.run(debug=True)