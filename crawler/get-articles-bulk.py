import requests
import json
from unicodedata import normalize
import re, string
import csv
import datetime
import time
import sys

url = 'http://api.nu.nl/v1.0/articles'

start_date = '2013-01-01T00:00:00'
start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')

offset_datetime = datetime.timedelta(minutes=5256)

with open('crawls-1.log', 'w') as crawlsfile:
    crawls_tsvwriter = csv.writer(crawlsfile, delimiter='\t')
    with open('article_list-1.tsv', 'w') as listfile:
        list_tsvwriter = csv.writer(listfile, delimiter='\t')
        for i in range(100):
            
            start_time_query = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            start_datetime = start_datetime + offset_datetime
            end_time_query = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            
            queries = {'clean_html':'iframe, script, style', 'updated_from' : str(start_time_query), 'updated_to' : str(end_time_query), 'limit' : '10000'}
            
            cnt=0
            max_retry=10
            while cnt < max_retry:
                article_request = requests.get('http://api.nu.nl/v1.0/articles/', auth = (u,p), params=queries)
                
                print article_request.status_code
                print article_request.url
                print start_time_query, end_time_query
                
                if article_request.status_code == requests.codes.ok:
                    cnt = max_retry
                    news_dict = article_request.json()
                    
                    print len(news_dict["results"])
                    
                    crawls_tsvwriter.writerow([str(start_time_query), str(end_time_query), len(news_dict["results"])])
                    
                    for item in news_dict["results"]:
                        list_tsvwriter.writerow([str(item['id'])])
                        with open('json_dumps/crawls_2013/' + str(item['id']) + '.article', 'w') as json_file:
                            json.dump(item, json_file, indent = 4)
                    
                else:
                    time.sleep(2**cnt)
                    cnt += 1
                    if cnt >= max_retry:
                        sys.exit('Error')
