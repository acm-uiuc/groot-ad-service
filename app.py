import subprocess
import os
from flask import Flask, jsonify, request, make_response
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

def verifyAddition(netid):
    execproc = subprocess.Popen([r'powershell.exe',
    './verify_ad_addition.ps1',
    netid], stdout=subprocess.PIPE, cwd=os.getcwd())
    out, err = execproc.communicate()
    if(out.decode().strip() == "1"):
        Users.query.filter_by(netid=netid).update(dict(added_to_directory=True))
        db.session.commit()
        return True

def runScript(netid):
    execproc = subprocess.Popen([r'powershell.exe',
    './user_creation_v2.ps1',
    netid], cwd=os.getcwd())
    result = execproc.wait()
    return result

@scheduler.scheduled_job('interval', days=1, next_run_time=datetime.now())
def addUserDaily():
    paidUsers = Users.query.filter_by(added_to_directory=False).filter_by(is_member=True).all()
    print(paidUsers)
    for user in paidUsers:
        runScript(user.netid)
        verifyAddition(user.netid)

@app.route("/activedirectory/add/<string:netid>")
def addUser(netid):
    if request.headers.get('Authorization') == SERVICE_ACCESS_TOKEN:
        output = runScript(netid)
        if(verifyAddition(netid)):
            return make_response(jsonify(dict(message=str("Added the user.")), 200)
        else:
            return make_response(jsonify(dict(error="There was an error.")), 400)

    else:
        return make_response(jsonify(dict(error="Please include the correct access token in the header.")), 401)

@app.route("/")
def root():
    return make_response(jsonify(dict(message="Welcome!")), 200)

db.init_app(app)
db.create_all(app=app)

if __name__ == "__main__":
    app.run(port=80, host='0.0.0.0')

# pip freeze > requirements.txt
