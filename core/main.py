from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Note(Resource):
    def get(self):
        return "Hello World!"


api.add_resource(Note, "/")

if __name__ == "__main__":
    app.run()
