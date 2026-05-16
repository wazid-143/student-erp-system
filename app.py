from flask import Flask

import database.db

from routes.auth import register_auth_routes
from routes.student import register_student_routes

app = Flask(__name__)

app.secret_key = "wazid"

# REGISTER ROUTES
register_auth_routes(app)
register_student_routes(app)

app.run(debug=True)