import controllers
from flask import request, Response, Blueprint

auth = Blueprint('auth', __name__)

@auth.route("/user/auth", methods=["POST"])
def auth_token_add() -> Response:
    return controllers.auth_token_add(request)