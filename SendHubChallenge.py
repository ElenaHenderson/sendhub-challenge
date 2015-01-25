from flask import Flask
from flask_restful import Api
from resources.Messages import Messages
from resources.Tests import Tests
from resources.Documentation import Documentation

app = Flask(__name__)
api = Api(app)

api.add_resource(Messages, '/messages')
api.add_resource(Tests, '/tests')
api.add_resource(Documentation, '/documentation')

if __name__ == '__main__':
    app.run()
