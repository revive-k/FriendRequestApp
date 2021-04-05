from flask import Flask, jsonify, request
import json
from api.User import User
from api.Friends import Friends

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/create', methods=['POST'])
def create_user():
	if not request.is_json:
		return jsonify({
			"status":"failure",
            "reason":"Body must be json"
		}), 400
	post_data = request.data
	data = json.loads(post_data)
	response, st_code = User().create_user(data)
	if st_code == 201:
		Friends().create_user_friends(data['username'])
	return response, st_code

@app.route('/add/<userA>/<userB>', methods=['POST'])
def send_request(userA, userB):
	return Friends().send_request(userA, userB)

@app.route('/friendRequests/<userA>')
def get_friend_requests(userA):
	return Friends().get_friend_requests(userA)

@app.route('/friends/<userA>')
def get_friends(userA):
	return Friends().get_friends(userA)

@app.route('/suggestions/<userA>')
def get_friends_suggestion(userA):
	return Friends().get_friends_suggestion(userA)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)