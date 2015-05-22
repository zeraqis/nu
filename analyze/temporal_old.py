#!/usr/bin/env python
import json
import datetime
import time
import pandas as pd

article_month_dict = {}
article_day_dict = {}
article_weekday_dict = {}

comment_month_dict = {}
comment_day_dict = {}
comment_weekday_dict = {}

with open('large.json','r') as jsonfile:
    json_dict = json.load(jsonfile)
    for item in json_dict:
        comment_datetime_list = []
        
        article_id = item['id']
        article_comment_count = 0
        
        published_at_str = item["article_dict"]["published_at"]
        published_at = datetime.datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%S')
        
        if published_at.month not in article_month_dict:
            article_month_dict[published_at.month] = 0
        article_month_dict[published_at.month] += 1
        
        if published_at.day not in article_day_dict:
            article_day_dict[published_at.day] = 0
        article_day_dict[published_at.day] += 1
        
        if published_at.weekday not in article_weekday_dict:
            article_weekday_dict[published_at.weekday] = 0
        article_weekday_dict[published_at.weekday] += 1
        
        for section in item['sections']:
            if 'canonical' in section:
                if section['style'] != None:
                    article_section = section['style']
                else:
                    article_section = section['name']
        
        for comment in item["comment_dict"]["comments"]:
            article_comment_count += 1
            
            curr_comment_time_str = comment["comment_ts"]
            curr_comment_time = datetime.datetime.strptime(curr_comment_time_str, '%Y-%m-%dT%H:%M:%S')
            
            comment_datetime_list.append(curr_comment_time)
            
            if curr_comment_time.month not in comment_month_dict:
                comment_month_dict[curr_comment_time.month] = 0
            comment_month_dict[curr_comment_time.month] += 1
            
            if curr_comment_time.day not in comment_day_dict:
                comment_day_dict[curr_comment_time.day] = 0
            comment_day_dict[curr_comment_time.day] += 1
            
            if curr_comment_time.weekday not in article_weekday_dict:
                article_weekday_dict[curr_comment_time.weekday] = 0
            article_weekday_dict[curr_comment_time.weekday] += 1
            
        first_comment = min(comment_datetime_list)
        last_comment = max(comment_datetime_list)
        
        interval_first = first_comment - published_at
        interval_last = last_comment - published_at
        interval_first_last = last_comment - first_comment
        
        