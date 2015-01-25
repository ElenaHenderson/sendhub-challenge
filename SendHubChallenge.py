from flask import Flask
from flask_restful import Api
from resources.Messages import Messages

app = Flask(__name__)
api = Api(app)

api.add_resource(Messages, '/messages')

if __name__ == '__main__':
    app.run()
