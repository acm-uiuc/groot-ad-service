import subprocess
import os
import logging
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from secrets import SERVICE_ACCESS_TOKEN, MYSQL
from datetime import datetime
from models import Users, db

app = Flask(__name__)


my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=5)
my_logger.addHandler(handler)


def verifyAddition(netid):
    execproc = subprocess.Popen([r'powershell.exe',
    './verify_ad_addition.ps1',
    netid], stdout=subprocess.PIPE, cwd=os.getcwd())
    out, err = execproc.communicate()
    my_logger.debug(out)
    my_logger.debug(err)
    if(out.decode().strip() == "1"):
        return True

def runScript(netid):
    execproc = subprocess.Popen([r'powershell.exe',
    './user_creation_v2.ps1',
    netid], cwd=os.getcwd())
    result = execproc.wait()
    my_logger.debug(result)
    return result


@app.route("/activedirectory/add/<string:netid>")
def addUser(netid):
    if request.headers.get('Authorization') == SERVICE_ACCESS_TOKEN:
        output = runScript(netid)
        if(verifyAddition(netid)):
            return make_response(jsonify(dict(message="Added the user.")), 200)
        else:
            return make_response(jsonify(dict(error="There was an error.")), 400)

    else:
        return make_response(jsonify(dict(error="Please include the correct access token in the header.")), 401)

@app.route("/")
def root():
    return make_response(jsonify(dict(message="Welcome!")), 200)


if __name__ == "__main__":
    app.run(port=80, host='0.0.0.0')

# pip freeze > requirements.txt
