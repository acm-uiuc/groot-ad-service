import subprocess
import os
from flask import Flask, jsonify, request, make_response
from secrets import SERVICE_ACCESS_TOKEN
from datetime import datetime
from models import Users, db

app = Flask(__name__)


def verifyAddition(netid):
    execproc = subprocess.Popen([r'powershell.exe',
                                './verify_ad_addition.ps1',
                                netid], stdout=subprocess.PIPE, cwd=os.getcwd())
    out, err = execproc.communicate()
    if(out.decode().strip() == "1"):
        return True
    return False


def runScript(netid):
    execproc = subprocess.Popen([r'powershell.exe',
                                './user_creation_v2.ps1',
                                netid], cwd=os.getcwd())
    result = execproc.wait()
    return result


@app.route("/activedirectory/add/<string:netid>")
def addUser(netid):
    if request.headers.get('Authorization') == SERVICE_ACCESS_TOKEN:
        output = runScript(netid)
        if(verifyAddition(netid)):
            return make_response(jsonify(dict(message=str("Added the user."))),
                                    200)
        else:
            return make_response(jsonify(dict(error="There was an error.")),
                                    400)

    else:
        return make_response(jsonify(dict(error="Please include the correct access token in the header.")),
                                401)


@app.route("/")
def root():
    return make_response(jsonify(dict(message="Welcome!")), 200)


db.init_app(app)
db.create_all(app=app)

if __name__ == "__main__":
    app.run(port=80, host='0.0.0.0')
