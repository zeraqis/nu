#!/usr/bin/env python
import json
import csv
from datetime import datetime
from eta import ETA
import random
import sys

threshold_time = datetime.strptime("December 1, 2014 00:00:00", "%B %d, %Y %H:%M:%S")
train_dict = {}
dev_dict = {}
train_user_list = []
dev_user_list = []

max_sample = 500
print 'loading json'

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nu/analyze/large.json','r') as jsonfile:
    json_dict = json.load(jsonfile)

print 'done'
eta = ETA(67225)
for item in json_dict:
    eta.print_status()
    if 'comments' in json_dict[item]["comment_dict"]:
        for comment in json_dict[item]["comment_dict"]["comments"]:
            curr_time_ts = json_dict[item]["comment_dict"]["comments"][comment]["comment_ts"]
            curr_time = datetime.strptime(curr_time_ts, "%B %d, %Y %H:%M:%S")
            user = json_dict[item]["comment_dict"]["comments"][comment]["author_id"]
            if json_dict[item]["comment_dict"]["comments"][comment]["comment_body"] != "":
                if curr_time < threshold_time:
                    if user not in train_dict:
                        train_dict[user] = {}
                        train_dict[user]['comments'] = {}
                    if curr_time_ts not in train_dict[user]['comments']:
                        train_dict[user]['comments'][curr_time_ts] = {}
                        #train_dict[user]['comments'][curr_time_ts]['co_commenters'] = []
                        train_user_list.append(user)
                    train_dict[user]['comments'][curr_time_ts]['body'] = json_dict[item]["comment_dict"]["comments"][comment]["comment_body"]
                    #train_dict[user]['comments'][curr_time_ts]['item'] = item
                    #for co_comment in json_dict[item]["comment_dict"]["comments"]:
                    #    if co_comment != comment:
                    #        co_user = json_dict[item]["comment_dict"]["comments"][co_comment]["author_id"]
                    #        if co_user != user:
                    #            train_dict[user]['comments'][curr_time_ts]['co_commenters'].append(co_user)
                if curr_time >= threshold_time:
                    if user not in dev_dict:
                        dev_dict[user] = {}
                        dev_dict[user]['comments'] = {}
                    if curr_time_ts not in dev_dict[user]['comments']:
                        dev_dict[user]['comments'][curr_time_ts] = {}
                        #dev_dict[user]['comments'][curr_time_ts]['co_commenters'] = []
                        dev_user_list.append(user)
                    dev_dict[user]['comments'][curr_time_ts]['body'] = json_dict[item]["comment_dict"]["comments"][comment]["comment_body"]
                    #dev_dict[user]['comments'][curr_time_ts]['item'] = item
                    #for co_comment in json_dict[item]["comment_dict"]["comments"]:
                    #    if co_comment != comment:
                    #        co_user = json_dict[item]["comment_dict"]["comments"][co_comment]["author_id"]
                    #        if co_user != user:
                    #            dev_dict[user]['comments'][curr_time_ts]['co_commenters'].append(co_user)
eta.done()

train_user_list = dev_user_list = set(train_user_list).intersection(set(dev_user_list))

train_final_dict = {}
dev_final_dict = {}

final_train_user_list = []

print "generating train dicts"
for user in train_dict:
    eta.print_status()
    if user in set(train_user_list) and len(train_dict[user]['comments']) > 5:
        if user not in set(final_train_user_list):
            final_train_user_list.append(user)
eta.done()

final_train_user_list = list(set(final_train_user_list))

#random.shuffle(final_train_user_list)

#final_train_user_list = final_train_user_list[0:max_sample]

for user in set(final_train_user_list):
    if user not in train_final_dict:    
        train_final_dict[user] = {}
        train_final_dict[user]['comments'] = {}
    for time in train_dict[user]['comments']:
        if time not in train_final_dict:
            train_final_dict[user]['comments'][time] = {}
        #train_final_dict[user]['comments'][time] = train_dict[user]['comments'][time]
        train_final_dict[user]['comments'][time]['body'] = train_dict[user]['comments'][time]['body']
        #train_final_dict[user]['comments'][time]['co_commenters'] = train_dict[user]['comments'][time]['co_commenters']
        #train_final_dict[user]['comments'][time]['item'] = train_dict[user]['comments'][time]['item']

final_dev_user_list = set(final_train_user_list)

print "generating dev dicts"
for user in set(final_dev_user_list):
    if user not in dev_final_dict:    
        dev_final_dict[user] = {}
        dev_final_dict[user]['comments'] = {}
    for time in dev_dict[user]['comments']:
        if time not in dev_final_dict:
            dev_final_dict[user]['comments'][time] = {}
        #dev_final_dict[user]['comments'][time] = dev_dict[user]['comments'][time]
        dev_final_dict[user]['comments'][time]['body'] = dev_dict[user]['comments'][time]['body']
        #dev_final_dict[user]['comments'][time]['co_commenters'] = dev_dict[user]['comments'][time]['co_commenters']
        #dev_final_dict[user]['comments'][time]['item'] = dev_dict[user]['comments'][time]['item']

print 'writing train list'
with open('train_users.tsv', 'w') as tsv_file:
    tsvwriter = csv.writer(tsv_file, delimiter = '\t')
    for train_user in train_final_dict:
        tsvwriter.writerow([train_user])

print 'writing dev list'
with open('dev_users.tsv', 'w') as tsv_file:
    tsvwriter = csv.writer(tsv_file, delimiter = '\t')
    for dev_user in dev_final_dict:
        tsvwriter.writerow([dev_user])

print 'writing train json'
with open("timed_train_full.json","w") as train_json_file:
    json.dump(train_dict, train_json_file, indent=4)

print 'writing dev json'    
with open("timed_dev_full.json","w") as dev_json_file:
    json.dump(dev_dict, dev_json_file, indent=4)

print 'writing train json'
with open("timed_train.json","w") as train_json_file:
    json.dump(train_final_dict, train_json_file, indent=4)

print 'writing dev json'    
with open("timed_dev.json","w") as dev_json_file:
    json.dump(dev_final_dict, dev_json_file, indent=4)
    