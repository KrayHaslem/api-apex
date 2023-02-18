import controllers
from flask import request, Response, Blueprint

contestants = Blueprint('contestants', __name__)

@contestants.route("/contestant", methods=["POST"])
def contestant_add() -> Response:
    return controllers.contestant_add(request)

@contestants.route("/contestant/get", methods=["GET"])
def contestants_get() -> Response:
    return controllers.contestants_get(request)

@contestants.route("/contestant/get/<contestant_id>", methods=["GET"])
def contestant_get(contestant_id) -> Response:
    return controllers.contestant_get(request, contestant_id)

@contestants.route("/contestant/<contestant_id>", methods=["POST", "PUT"])
def contestant_update(contestant_id) -> Response:
    return controllers.contestant_upate(request, contestant_id)

