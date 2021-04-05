import json
import collections
from flask import jsonify

class User:

    def path_to_user_file(self):
        with open('config.json', 'r') as file:
            file = json.load(file)
        return file["user_path"]

    def read_user_file(self):
        path_to_file = self.path_to_user_file()
        with open(path_to_file, 'r') as json_file:
            user_json_file = json.load(json_file)
        return user_json_file

    def write_user_json_file(self, user_json_file):
        path_to_file = self.path_to_user_file()
        with open(path_to_file, 'w') as file_user:
            json.dump(user_json_file, file_user)

    def get_usernames(self):
        usernames = []
        user_file = self.read_user_file()
        for user in user_file:
            usernames.append(user['username'])
        return usernames

    def create_user(self, user_input):
        for key in ["username"]:
            if key not in user_input:
                return jsonify({
					'status': 'failure',
                    'reason': 'Input should contain username'
				}), 400
        user_names = self.get_usernames()
        if user_input['username'] in user_names:
            return jsonify({
                'status': 'failure',
                'reason': 'Username already exists'
            }), 400
        user_json_file = self.read_user_file()
        user_json_file.append(user_input)
        self.write_user_json_file(user_json_file)
        return jsonify({
            'username': user_input['username']
        }), 201