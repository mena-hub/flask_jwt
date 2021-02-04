from flask_restful import Resource
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity

class AccountSettings(Resource):
    @fresh_jwt_required
    def post(self):
        username = get_jwt_identity()
        # Important setting change commits 