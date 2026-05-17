from flask import Flask

import database.db

from routes.auth import register_auth_routes
from routes.student import register_student_routes

app = Flask(__name__)

app.secret_key = "wazid"

# REGISTER ROUTES
register_auth_routes(app)
register_student_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)