from flask.ext.restful import Resource
from flask import send_file


class Documentation(Resource):
    def get(self):
        return send_file('documentation.html')
