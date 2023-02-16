import controllers
from flask import request, Response, Blueprint

app_users = Blueprint('app_users', __name__)

@app_users.route("/users", methods=["POST"])
def user_add() -> Response:
    return controllers.user_add(request)
