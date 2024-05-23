from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('api.api.config.Config')  # Ensure this path is correct

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your routes and models to register them with the Flask app
from api.api import routes, models
