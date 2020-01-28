from flask import Flask, jsonify, request, redirect, session, render_template
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from flask_cas import login_required, CAS, login, logout
from flask_cors import CORS
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import pymongo
from bson.json_util import dumps
import json
from urllib.parse import quote_plus
from pymongo.errors import ConnectionFailure


mongo = pymongo.MongoClient('mongodb+srv://paulo892:hello@cluster0-farth.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=False)

db = pymongo.database.Database(mongo, 'idioma')
users = pymongo.collection.Collection(db, 'users')
#user_results = json.loads(dumps(users.find().limit(5).sort("email", -1)))
user_results = 'HELLO'

# testing


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__, static_folder='../build/static', template_folder='../build/')

app.config.from_object(__name__)

#app.json_encoder = MyJSONEncoder
#app.config['MONGO_DBNAME'] = 'idioma'
#app.config['MONGO_URI'] = 'mongodb+srv://paulo892:<LORu0a9ZqjMx5t2J>@cluster0-farth.mongodb.net/test?retryWrites=true&w=majority'

#client = pymongo.MongoClient("mongodb+srv://paulo892:<password>@cluster0-farth.mongodb.net/test?retryWrites=true&w=majority")
#db = client.test
#mongo = PyMongo(app)
CORS(app)

#session_opts = {
#    'session.type': 'file',
#    'session.cookie_expires': True,
#    'session.data_dir': './data',
#    'session.auto': True
#}

#session_opts = {
#    'session.type': 'file',
#    'session.cookie_expires': True,
#    'session.data_dir': './data',
#    'session.auto': True
#}

#class BeakerSessionInterface(SessionInterface):
#	def open_session(self, app, request):
#		session = request.environ['beaker.session']
#		return session
#
#	def save_session(self, app, session, response):
#		session.save()

# secret key
#secret_key = environ.get('SECRET_KEY', "uhuhuhuhuhuhiwannaerykahbadu")
#app.secret_key = secret_key

#app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
#app.session_interface = BeakerSessionInterface()

@app.route('/api/getUsers', methods=['GET'])
def get_users():

    try:
        #cursor = mongo.db.users.find()
        #users = []
        #for user in cursor:
        #    users.append(user)
        return jsonify(user_results)
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # print(_get_user_meal_data("5bf8ca12e7179a56e21592c5", "2018-07-11", "lunch"))
    # print(_get_user_meal_data("5bf8ca12e7179a56e21592c5", "2018-07-11", "breakfast"))
    # print(_get_user_meal_data("5bf8ca12e7179a56e21592c5", "2018-07-13", "breakfast"))
    # print(_get_user_nutrient_progress("5bf8ca12e7179a56e21592c5", "2018-07-11", "2018-07-15"))
    # print(_get_user('5bf8ca12e7179a56e21592c5'))
    # print(change_nutrition_goals('5bf8ca12e7179a56e21592c5', 68, 4, 4, 4))
    # print(_get_user_nutrient_progress('5bf8ca12e7179a56e21592c5', '2018-11-01', '2019-01-02'))
    # print(verify_login("isinha@princeton.edu", "password"))
    # print(verify_login("isinhasda@princeton.edu", "password"))
    # print(_get_user_meal_notes('5bf8ca12e7179a56e21592c5', '2019-01-05', 'breakfast'))
    # print(_get_user_day_meal_notes('5bf8ca12e7179a56e21592c5', '2019-01-05'))
    # print(change_mealnote("5bf8ca12e7179a56e21592c5", "2019-01-05", "lunch", "asfopiajw"))

    # lp = LineProfiler()
    # lp_wrapper = lp(get_user_nutrient_progress_all_new)
    # lp_wrapper('5bf8ca12e7179a56e21592c5')
    # lp.print_stats()





    print('hi')
    print('ypo')
    app.run(debug=True)