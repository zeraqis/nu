#!/usr/bin/env python
import json
import csv

def analyze_json(json, string):
    user_count = 0
    item_list = []
    comment_count = 0
    user_count = len(json)
    with open(string + '_user-comment_count.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for user in json:
            csvwriter.writerow([user, len(json[user]['comments'])])
            comment_count += len(json[user]['comments'])
    return [string, user_count, comment_count]

with open('analyze_split.tsv','w') as tsvfile:
    tsvwriter = csv.writer(tsvfile, delimiter = '\t')
    tsvwriter.writerow(['set', 'user_count', 'comment_count'])
    
    print 'loading train'
    with open('timed_train.json', 'r') as train_json:
        train_dict = json.load(train_json)
        tsvwriter.writerow(analyze_json(train_dict, 'train'))
    
    print 'loading test'
    with open('timed_dev.json', 'r') as dev_json:
        dev_dict = json.load(dev_json)
        tsvwriter.writerow(analyze_json(dev_dict, 'dev'))