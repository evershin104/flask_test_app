import os
from app import create_app, db
from flask_migrate import upgrade

DB_PATH = os.path.join(os.path.dirname(__file__), "app", "instance", "test.db")


app = create_app()

with app.app_context():
    upgrade()

if __name__ == "__main__":
    app.run(debug=True)
