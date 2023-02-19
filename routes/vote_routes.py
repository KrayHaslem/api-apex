import controllers
from flask import request, Response, Blueprint

votes = Blueprint('votes', __name__)

@votes.route("/votes", methods=["POST"])
def vote_add() -> Response:
    return controllers.vote_add(request)

@votes.route("/votes", methods=["GET"])
def get_votes() -> Response:
    return controllers.get_votes(request)

@votes.route("/votes/verify/<vote_id>", methods=["POST"])
def verify_vote(vote_id) -> Response:
    return controllers.verify_vote(request, vote_id)

@votes.route("/votes/count", methods=["GET"])
def vote_count() -> Response:
    return controllers.vote_count(request)