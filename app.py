import subprocess, os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from secrets import SERVICE_ACCESS_TOKEN, MYSQL
from datetime import datetime
from models import Users, db

scheduler = BackgroundScheduler()
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    MYSQL['user'],
    MYSQL['password'],
    MYSQL['host'],
    MYSQL['dbname']
)

def runScript(netid):
    execproc = subprocess.Popen([r'powershell.exe',
                                 './user_creation.ps1',
                                 netid], cwd=os.getcwd())
    result = execproc.wait()
    return result



@scheduler.scheduled_job('interval', days=1, next_run_time=datetime.now())
@app.route("/adduser/test")
def addUserDaily():
	paidUsers = Users.query.filter_by(added_to_directory=False).filter_by(is_member=True).all()
	
	for user in paidUsers:
		runScript(user.netid)
		Users.query.filter_by(netid=user.netid).update({added_to_directory=True})
		Users.commit()
	return 1

@app.route("/adduser/<string:netid>")
def addUser(netid):
	# request.headers['your-header-name']
    return runScript(netid)

@app.route("/")
def root():
	return ""

db.init_app(app)
db.create_all(app=app)

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')

# pip freeze > requirements.txt 

