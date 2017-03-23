from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_member = db.Column(db.Boolean, default=False)
    netid = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    uin = db.Column(db.Integer, unique=True)
    added_to_directory = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'is_member': self.is_member,
            'netid': self.netid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'uin': self.uin,
            'added_to_directory': self.added_to_directory,
            'created_at': self.created_at.isoformat(),
        }
        return user_dict


# +--------------------+------------------+------+-----+---------+----------------+
# | Field              | Type             | Null | Key | Default | Extra          |
# +--------------------+------------------+------+-----+---------+----------------+
# | id                 | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
# | is_member          | tinyint(1)       | YES  |     | 0       |                |
# | netid              | varchar(50)      | NO   | UNI | NULL    |                |
# | first_name         | varchar(50)      | NO   |     | NULL    |                |
# | last_name          | varchar(50)      | NO   |     | NULL    |                |
# | uin                | int(11)          | YES  | UNI | NULL    |                |
# | added_to_directory | tinyint(1)       | YES  |     | 0       |                |
# | created_at         | datetime         | YES  |     | NULL    |                |
# +--------------------+------------------+------+-----+---------+----------------+
