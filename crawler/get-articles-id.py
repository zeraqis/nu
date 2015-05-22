import requests
import json
from unicodedata import normalize
import re, string
import csv
from math import ceil

article_list = []
with open('TNO_testdata_11_02_2015.csv', 'r') as csvfile:
	next(csvfile)
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		article_id = row[-1]
		if article_id[0] == '/':
			article_id = article_id.split('/')[2]
		article_list.append(article_id)

url = 'http://api.nu.nl/v1.0/articles'

article_list = list(set(article_list))
slices = int(ceil(len(article_list)/500.0))
print slices

for i in range(slices):
	article_list_str = ','.join(article_list[i*500:(i+1)*500])
	print i*500,(i+1)*500
	article_request = requests.get('http://api.nu.nl/v1.0/articles/id/' + article_list_str + '/', auth = (u,p))
	
	print article_request.status_code
	print article_request.url
	
	news_dict = article_request.json()
	
	for item in news_dict["results"]:
		with open('json_dumps/TNO_testdata_11_02_2015/' + str(item['id']) + '.article', 'w') as json_file:
			json.dump(item, json_file, indent = 4)

# for item in news_dict["results"]:
	# count+=1
	# title = item["title"]
	# comment_count = item["social_counts"]["nujij_comments"]
	# if comment_count > 0:
		# print title
		# article_url = item["url"]
		# print article_url
