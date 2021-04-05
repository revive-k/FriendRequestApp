import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import json
from flask import jsonify
from User import User

class Friends:

	def path_to_file_friends(self):
		with open('config.json', 'r') as file:
			file = json.load(file)
		return file["friends_path"]
	
	def read_friends_file(self):
		path_to_file = self.path_to_file_friends()
		with open(path_to_file, 'r') as json_file:
			friends_json_file = json.load(json_file)
		return friends_json_file

	def write_friends_json_file(self, friends_json_file):
		path_to_file = self.path_to_file_friends()
		with open(path_to_file, 'w') as file_friends:
			json.dump(friends_json_file, file_friends)

	def create_user_friends(self, myuser):
		json_file = self.read_friends_file()
		user_friends = {
			"username": myuser,
			"friendRequests": [],
			"friends":[]
		}
		json_file.append(user_friends)
		self.write_friends_json_file(json_file)

	def get_friend_requests(self, userA):
		json_file = self.read_friends_file()
		usernames = User().get_usernames()
		if userA not in usernames:
			return jsonify({
				'status': 'failure',
				'reason': "User doesn't exist"
			}), 400  
		user_fdreq = []
		for user in json_file:
			if user['username'] == userA:
				user_fdreq = user['friendRequests']
		if len(user_fdreq)==0:
			return jsonify({
				'status': 'failure',
				'reason': "No pending friend requests"
			}), 404 
		return jsonify({
				'friend_requests': user_fdreq
			}), 200

	def get_friends(self, userA):
		json_file = self.read_friends_file()
		usernames = User().get_usernames()
		if userA not in usernames:
			return jsonify({
				'status': 'failure',
				'reason': "User doesn't exist"
			}), 400  
		user_friends = []
		for user in json_file:
			if user['username'] == userA:
				user_friends = user['friends']
		if len(user_friends)==0:
			return jsonify({
				'status': 'failure',
				'reason': "No friends found"
			}), 404 
		return jsonify({
				'friends': user_friends
			}), 200

	def get_friends_suggestion(self, userA):
		json_file = self.read_friends_file()
		usernames = User().get_usernames()
		if userA not in usernames:
			return jsonify({
				'status': 'failure',
				'reason': "User doesn't exist"
			}), 400  

		friend_sugg = []
		userfriends = []
		for user in json_file:
			if user['username'] == userA:
				userfriends = user['friends']

		for user in json_file:	
			for frds in userfriends:
				if user['username'] == frds:
					firstdegfrnds = user['friends']
					for fr in firstdegfrnds:
						if fr != userA and fr not in userfriends:
							friend_sugg.append(fr)

		for user in json_file:	
			for frds in friend_sugg:
				if user['username'] == frds:
					seconddegfrnds = user['friends']
					for fr in seconddegfrnds:
						if fr != userA and fr not in userfriends:
							friend_sugg.append(fr)

		friend_sugg_ans = []
		for item in friend_sugg:
			if item not in friend_sugg_ans:
				friend_sugg_ans.append(item)

		if len(friend_sugg_ans)==0:
			return jsonify({
				'status': 'failure',
				'reason': "No friends suggestions"
			}), 404 
		return jsonify({
				'suggestions': friend_sugg_ans
			}), 200

	def send_request(self, userA, userB):
		usernames = User().get_usernames()
		if (userA not in usernames or userB not in usernames):
			return jsonify({
				'status': 'failure',
				'reason': "User doesn't exist"
			}), 400
		
		json_file = self.read_friends_file()
		userAfriends = []
		userBfriends = []
		userAfriendreq = []
		userBfriendreq = []
		for user in json_file:
			if user['username'] == userB:
				userBfriends = user['friends']
				userBfriendreq = user['friendRequests']
			if user['username'] == userA:
				userAfriends = user['friends']
				userAfriendreq = user['friendRequests']
		
		if (userA in userBfriends or userA in userBfriendreq):
			return jsonify({
				'status': 'failure',
				'reason': "Friend Request sent already"
			}), 400

		if userB in userAfriendreq:
			userAfriendreq.remove(userB)
			userAfriends.append(userB)
			userBfriends.append(userA)
		else:
			userBfriendreq.append(userA)

		for user in json_file:
			if user['username'] == userB:
				user['friends'] = userBfriends
				user['friendRequests'] = userBfriendreq
			if user['username'] == userA:
				user['friends'] = userAfriends
				user['friendRequests'] = userAfriendreq

		self.write_friends_json_file(json_file)
		return jsonify({
			"status": "success"
		}), 202