#!/usr/bin/python3
'''
	A Gomes 2017/09
	gomes.bcc@gmail.com
'''
from __future__ import print_function
import requests
import time
import json
import sys
import os


info = {
	"filesdir": "/home/stories",
	"ids": {
		"<REAL_ID>": "<GIVEN_NAME>",
		"<REAL_ID>": "<GIVEN_NAME>"
		}
    }
    
headers = {
	"cookie": "<YOUR_COOKIE>",
	"user-agent": "Instagram 12.0.0.7.91 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+",
	"cache-control": "no-cache"
}


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


print("[{}] Looking for new data.".format(time.strftime("%Y/%m/%d-%H:%M:%S")))

while len(info["ids"]) > 0:
	pair = info["ids"].popitem()
	response = requests.request("GET", "https://i.instagram.com/api/v1/feed/user/"+pair[0]+"/reel_media/", headers=headers)
	if response.status_code != 200:
		print("[!] ERROR: "+str(response.status_code)+" response status.", file=sys.stderr)
		exit
	response = json.loads(response.text)
	for item in response['items']:
		item_id = item['id']
		
		if item["media_type"] == 1: # Photo
			url = item['image_versions2']['candidates'][0]['url']
			filename = str(item['taken_at']) + ".jpg"
		if item["media_type"] == 2: # Video
			url = item['video_versions'][0]['url']
			filename = str(item['taken_at']) + ".mp4"
		
		try:
			r = requests.get(url)
			
			if r.status_code == 404:
				print("[!] Error 404 on URL: " + url, file=sys.stderr)
			elif r.status_code%200 < 100:
				save_file(filename, r, folder_name=pair[1])
		except Exception as e:
			print("[!] Unknow error: " + str(e))
