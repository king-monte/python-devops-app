from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import time

app = Flask(__name__)

DB_USER = os.getenv("POSTGRES_USER", "devops")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "flaskdb")
DB_HOST = os.getenv("DB_HOST", "db")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

db = SQLAlchemy(app)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.route('/')
def home():
    return "Flask + PostgreSQL + Docker + CI/CD 🚀"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200


if __name__ == '__main__':

    retries = 5

    while retries > 0:
        try:
            with app.app_context():
                db.create_all()

            print("Database connected successfully!")
            break

        except Exception as e:
            print(f"Database not ready: {e}")

            retries -= 1
            time.sleep(5)

    app.run(host='0.0.0.0', port=5000)