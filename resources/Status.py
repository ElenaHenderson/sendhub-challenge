from flask.ext.restful import Resource
from flask import send_file


class Status(Resource):
    def get(self):
        return send_file('test.html')


