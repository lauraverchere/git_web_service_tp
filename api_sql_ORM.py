from datetime import datetime
from sqlalchemy import create_engine, text
from faker import Faker
from flask import Flask, jsonify
import random
from flask_sqlalchemy import SQLAlchemy





# Configuration de la base de données
db_string = "postgresql://root:root@localhost:5432/postgres"
engine = create_engine(db_string)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

@app.route("/user")
def get_user():
    results = Users_ORM.query.all()
    data = []
    for row in results:
        user = {
            "id": row.id,
            "firstname": row.firstname,
            "lastname": row.lastname,
            "age": row.age,
            "email": row.email,
            "job": row.job
        }
        data.append(user)
    return jsonify(data)

# Définition de la classe Users
class Users_ORM (db.Model) : 
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer())
    email = db.Column(db.String(200))
    job = db.Column(db.String(100))
                      
    def __init__(self, firstname, lastname, age, email, job):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.job = job


# Définition de la classe Applications
class Applications_ORM (db.Model) : 
    id = db.Column(db.Integer, primary_key = True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.TIMESTAMP(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users_orm.id'))

    def __init__(self, appname, username, lastconnection, user_id) : 
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnection
        self.user_id = user_id


fake = Faker()

def populate_tables():
    applications = ["Facebook", "Instagram", "Twitter", "Airbnb", "TikTok", "LinkedIn"]
    for n in range(100):
        firstame = fake.first_name()
        lastname = fake.last_name()
        age = random.randrange(18, 50)
        email = fake.email()
        job = fake.job()
        user = Users_ORM(firstame, lastname, age, email, job)
        db.session.add(user)
        db.session.commit()
        
        user_id = user.id

        apps_names = [random.choice(applications) for n in range(1, random.randrange(1, 5))]
        for app_name in apps_names:
            username = fake.user_name()
            lastconnection = datetime.now()
            new_app = Applications_ORM (app_name, username, lastconnection, user_id)
            db.session.add(new_app)
            db.session.commit()

            
        
if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        populate_tables()
        app.run(host="0.0.0.0", port=8081)

    
    
    
    
    

