from flask import Flask
from flask_restful import Api
from resources.Messages import Messages
from resources.Status import Status

app = Flask(__name__)
api = Api(app)

api.add_resource(Messages, '/messages')
api.add_resource(Status, '/')

if __name__ == '__main__':
    app.run()
