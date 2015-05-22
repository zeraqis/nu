import requests
from bs4 import BeautifulSoup
import re
import os
import json
from math import ceil
import sys
import csv

regex = re.compile(r'[\n\r\t]')

with open('comment_counts/counts_' + str(sys.argv[1]) + '.csv', 'w') as csvfile:
    log_writer = csv.writer(csvfile)
    with open('article_list_2014/list_' + str(sys.argv[1]), 'r') as list_file:
        list_reader = csv.reader(list_file, delimiter='\t')
        for row in list_reader:
            file_dir = 'json_dumps/crawls_2014/' + str(row[0]) + '.article'
            with open(file_dir, 'r') as json_file:
                item = json.load(json_file)
                status = ''
                while status != '200':
                    article_request = requests.get(item['url'])
                    print article_request.status_code, article_request.url
                    status = str(article_request.status_code)
                article_soup = BeautifulSoup(article_request.text, "html5lib")
                divs_social = article_soup.findAll('div', class_='socialbar-wrapper with-counters')
                for div in divs_social:
                    a = div.find('li', class_="nujij").find('a')
                    actual_count = a.find('span', class_="counter").contents[0]
                api_count = item["social_counts"]["nujij_comments"]
                print item['id'], article_request.url, actual_count, api_count
                log_writer.writerow([item['id'], article_request.url, actual_count, api_count])