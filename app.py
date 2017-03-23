import subprocess, os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from setting import SERVICE_ACCESS_TOKEN


app = Flask(__name__)

@scheduler.scheduled_job('interval', days=1, next_run_time=datetime.now())
def addUserDaily():
	# sql query
	select * from users where added_to_directory=0 AND is_member=1;
	update groot_user_service.users set added_to_directory=1 where netid=<netid>;




@app.route("/adduser/<string:netid>")
def addUser(netid):
    execproc = subprocess.Popen([r'powershell.exe',
                                 './user_creation.ps1',
                                 netid], cwd=os.getcwd())
    result = execproc.wait()

    return str(result)

@app.route("/")
def root():
	return 200

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')

pip freeze > requirements.txt 

