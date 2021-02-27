#source venv/bin/activate
#pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy pymysql
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm.attributes import flag_modified

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Bgbb1512#@localhost/prueba"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(45))
    password = db.Column(db.String(45))
    
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('idUser', 'userName', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

@app.route('/Users', methods = ["POST"])
def createUser():
    uname = request.json["Username"]
    pwd = request.json["Password"]
    new_usr = User(uname, pwd)
    db.session.add(new_usr)
    db.session.commit()
    return user_schema.jsonify(new_usr)

@app.route('/Users', methods = ["GET"])
def getUsers():
    all_users = User.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)

@app.route('/Users/<id>', methods = ["GET"])
def getUser(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/Users/<id>', methods = ["PUT"])#PATCH
def updateUser(id):
    user = User.query.get(id)
    uname, pwd = request.json["Username"], request.json["Password"]
    user.userName, user.password = uname, pwd
    flag_modified(user, "userName")
    flag_modified(user, "password")
    db.session.merge(user)
    db.session.flush()
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/Users/<id>', methods = ["DELETE"])
def deleteUser(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/', methods = ["GET"])
def index():
    return jsonify({'message': 'Welcome to my API.'})

if __name__ == "__main__":
    app.run(debug = True)