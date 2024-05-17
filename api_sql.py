from datetime import datetime
from sqlalchemy import create_engine, text
from faker import Faker
from flask import Flask, jsonify
import random

db_string = "postgresql://root:root@localhost:5432/postgres"

engine = create_engine(db_string)
app = Flask(__name__)
@app.route("/home", methods=["GET"])

def get_users() : 
    users = run_sql_with_result("SELECT * FROM users")
    data = []
    for row in users : 
        user = {
            "id" : row[0], 
            "firstname": row[1], 
            "lastname": row[2], 
            "age" : row[3], 
            "email" : row[4], 
            "job" : row[5]
        }
        data.append(user)
    return jsonify(data)

create_user_table ="""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    age INT,
    email VARCHAR(200),
    job VARCHAR(100)
    );
    """

create_apps_table ="""
CREATE TABLE IF NOT EXISTS application (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(100),
    username VARCHAR(100),
    lastconnection TIMESTAMP WITH TIME ZONE,
    user_id INTEGER REFERENCES users(id)
    );
    """


def populate_tables():
    faker = Faker('fr_FR')
    app = ["Instagram", "Facebook", "LinkedIn", "Airbnb", "Tik Tok"]
    for i in range(0, 100):
        firstname = faker.first_name()
        lastname = faker.last_name()
        age = random.randrange(18, 60)
        email = faker.ascii_free_email()
        job = faker.job().replace("'", "")

        add_users = f"""
            INSERT INTO users (firstname, lastname, age, email, job) 
            VALUES ('{firstname}', '{lastname}', {age}, '{email}', '{job}')
            RETURNING id
        """
        user_id = run_sql_with_result(add_users).scalar() #.scalar() pour récupérer l'id 
        #print(user_id)


        # Get number of app for current user
        num_apps = random.randint(1, 5)
        for i in range(num_apps) : 
            # For each app, insert a new app in the DB
            username = faker.user_name()
            lastconnection = datetime.now()
            app_name = random.choice(app)

            add_app = f""" 
                INSERT INTO application (appname, username, lastconnection, user_id) 
                VALUES ('{app_name}', '{username}', '{lastconnection}', {user_id})
            """
            run_sql(add_app)



def run_sql_with_result(query: str):
    with engine.connect() as connection:
        trans = connection.begin()  
        result = connection.execute(text(query))
        trans.commit() 
        return result 

def run_sql(query: str):
    with engine.connect() as connection:
        trans = connection.begin()  
        connection.execute(text(query))
        trans.commit() 

if __name__ == "__main__":
    run_sql(create_user_table)
    run_sql(create_apps_table)
    populate_tables()
    #app.run(host="0.0.0.0", port=8081)
