from flask import Flask
from flask_recaptcha import ReCaptcha
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

app.config['RECAPTCHA_SITE_KEY'] = '6LcIEeIgAAAAAMjypLNll4TLQFyOscswLP1HME2p' 
app.config['RECAPTCHA_SECRET_KEY'] = '6LcIEeIgAAAAAPdgrg_om-RqkOrpzqtgMCu2-9_R'
recaptcha = ReCaptcha(app)

client = MongoClient("mongodb+srv://Cluster36756:bVhuXUFvbFxl@cluster36756.ww1d8qu.mongodb.net/?retryWrites=true&w=majority")
db = client['CongressionalDB']
surveys = db['Surveys']
conversations = db['Conversations']
turkers = db['Turkers']
blueprints = db['Blueprints']
logs = db['Logs']

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)