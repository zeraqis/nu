import csv
import json
from eta import ETA
import json
import os

sub_dir = '/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nu/crawler/json_dumps/crawls_2014/'
list_dir = '/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nu/crawler/article_list_2014/'
large_json = {}

#sections = {''}

eta = ETA(20)

for i in range(20):
    eta.print_status()
    with open(list_dir + 'list_' + str(i)) as list_file:
        list_reader = csv.reader(list_file, delimiter='\t')
        for row in list_reader:
            article_id = str(row[0])
            if article_id not in large_json:
                large_json[article_id] = {}
                large_json[article_id]['article_dict'] = {}
                large_json[article_id]['comment_dict'] = {}
            article_dir = sub_dir + row[0] + '.article'
            with open(article_dir, 'r') as article_file:
                article = json.load(article_file)
                large_json[article_id]['article_dict'] = article
                comment_dir = sub_dir + row[0] + '.comment'
                if os.path.isfile(comment_dir):
                    with open(comment_dir, 'r') as comment_file:
                        comment_dict = json.load(comment_file)
                    large_json[article_id]['comment_dict'] = comment_dict
eta.done()
with open('large.json', 'w') as large_json_file:
    json.dump(large_json, large_json_file, indent=4)