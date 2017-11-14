import requests
import json
import sys
import os
#from __future__ import print_function
import time

info = {
	"filesdir": "/path/",
	"ids": {
		"290228823": "random"
	}
}

headers = {
	"cookie": "<COOKIE-HERE>"
	"user-agent": "Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+",
	"cache-control": "no-cache",
	"x-ig-capabilities": "36oD"
}


def next_page(data, userid):
	if 'user' in data:
		page_info = data['user']['media']['page_info']
		
	elif 'data' in data:
		page_info = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]
	else:
		print("[!] Unrecognized data structure.")
		return None
		
	if page_info["has_next_page"]:
		end_cursor = page_info["end_cursor"]
		response = requests.request("GET", "https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables={\"id\":\""+userid+"\",\"first\":12,\"after\":\""+end_cursor+"\"}", headers=headers)
	else:
		print("[!] No more pages.")
		return None
	
	
	if response.status_code != 200:
		print("[!] Error in 'next_page'. status_core != 200.")
		return None
	else:
		req = json.loads(response.text)
		
	return req
	
	
def get_nodes(data):
	if 'user' in data:
		return data['user']['media']['nodes']
	elif 'data' in data:
		tmp = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
		nodes = list()
		for i in tmp:
			nodes.append(i['node'])
		return nodes
		
	else:
		print("[!] Unrecognized data structure.")
		return None


def get_url_filename(node):
	url = None
	filename = None
	
	if node["is_video"]:
		filename = node["id"] + ".mp4"
	else:
		filename = node["id"] + ".jpg"
		
	if 'display_src' in node:
		url = node["display_src"]
	elif 'display_url' in node:
		url = node["display_url"]
	else:
		print("[!] Unrecognized data structure.")
	
	return url, filename
	
def save_file(file_name, req, folder_name= ""):
	try:
		if folder_name:
			folder = folder_name + "/"
		folder_path = info["filesdir"] + "/" + folder
		file_path = folder_path+file_name
		
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		elif os.path.isfile(file_path):
			return False

		with open(file_path, 'wb') as f:
			for chunk in req.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
				
		print('"' + file_path + '" saved.')
		return True
	except Exception as e:
		print("[!] Error while trying to save file " + file_path, file=sys.stderr)
		return False


class IUser:
	
	def __init__(self):
		self.username = None
		self.userid = None
		self.user = None

	def get_info(self, insta_id):
		response = requests.request("GET", "https://i.instagram.com/api/v1/feed/user/"+insta_id+"/reel_media/", headers=headers)
		if response.status_code != 200:
			print("[!] Error in 'get_info'.")
			return None
		
		payload = json.loads(response.text)
		self.user = payload["user"]
		self.username = payload["user"]["username"]
		

	def get_all_media(self, insta_id):
		self.userid = insta_id
		if self.username is None:
			self.get_info(self.userid)
			
		response = requests.request("GET", "https://www.instagram.com/"+self.username+"/?__a=1", headers=headers)
		if response.status_code != 200:
			print("[!] Error in 'get_all_media'. ")
			return None
			
		payload = json.loads(response.text)
		media = payload["user"]["media"]
		total_media = media["count"]
		
		
		print("Images to download: {}".format(total_media))
		down_count = 0
		
		while (down_count < total_media):
			print("[!] Next 12. ({}/{})".format(down_count, total_media))
			nodes = get_nodes(payload)
			
			for node in nodes:
                                # TODO: Get nodes of nodes (multiple pics at one post)
				url, filename = get_url_filename(node)
				r = requests.get(url)
				
				if r.status_code == 404:
					print("[!] Error 404 on URL: " + url, file=sys.stderr)
				elif r.status_code%200 < 100:
					save_file(filename, r, folder_name=self.username)
					down_count += 1
			
			payload = next_page(payload, self.userid)
			time.sleep(2)
			if not payload:
				break
			
		print("[!] Stopping downloads. ({}/{})".format(down_count, total_media))

# Example:
#t = IUser()
#t.get_all_media("<USER_ID>")

