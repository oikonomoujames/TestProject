from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import os
from subprocess import call
import subprocess

app = Flask(__name__)
api = Api(app)


class Users(Resource):

    def get(self):
        data = pd.read_csv('users.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code

class Directory(Resource):

    def get(self):
        # stdout=subprocess.PIPE tells Python to redirect the output of the command to an object so it can be manually read later
        # Add error checking
        data = subprocess.run(["ls", "-l"], stdout=subprocess.PIPE, text=True)
        return data.__dict__, 200

class Locations(Resource):
    # methods go here
    pass


api.add_resource(Users, '/users')  # '/users' is our entry point
api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations
api.add_resource(Directory, '/directory')

if __name__ == '__main__':
    app.run()  # run our Flask app
