from flask.ext.restful import Resource
from flask import send_file


class Tests(Resource):
    def get(self):
        return send_file('tests.html')