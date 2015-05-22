#!/usr/bin/env python
import json
import datetime
import time
import pandas as pd
import math
import numpy as np
from eta import ETA

analyze_df = pd.DataFrame()
analyze_df['published_at'] = []
analyze_df['published_year'] = []
analyze_df['published_month'] = []
analyze_df['published_day'] = []
analyze_df['published_weekday'] = []
analyze_df['published_hour'] = []
analyze_df['comment_count'] = []
analyze_df['interval_first'] = []
analyze_df['interval_last'] = []
analyze_df['interval_first_last'] = []
analyze_df['article_section'] = []
analyze_df['article_name'] = []
analyze_df['clicks'] = []
analyze_df['article_length'] = []
analyze_df['published_comments'] = []

user_df = pd.DataFrame()
user_df['user_id'] = []
user_df['article_id'] = []
user_df['comment_count'] = []
user_df['reply_count'] = []

user_dict = {}

with open('large.json','r') as jsonfile:
    json_dict = json.load(jsonfile)
    eta = ETA(67225)
    for item in json_dict:
	eta.print_status()
	comment_datetime_list = []
        
        article_id = json_dict[item]["article_dict"]['id']
        article_comment_count = 0
        
        published_at_str = json_dict[item]["article_dict"]["published_at"]
        published_at = datetime.datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%S')
        analyze_df = analyze_df.append(pd.DataFrame({'published_at' : [published_at_str]}, index = [article_id]))
        
        user_df = user_df.append(pd.DataFrame({'user_id' : []}))
        
	analyze_df.ix[article_id, 'published_year'] = published_at.year
        analyze_df.ix[article_id, 'published_month'] = published_at.month
        analyze_df.ix[article_id, 'published_day'] = published_at.day
	analyze_df.ix[article_id, 'published_weekday'] = published_at.weekday()
	analyze_df.ix[article_id, 'published_hour'] = published_at.hour
	analyze_df.ix[article_id, 'published_comments'] = json_dict[item]["article_dict"]["social_counts"]["nujij_comments"]
        
        analyze_df.ix[article_id, 'article_length'] = len(json_dict[item]["article_dict"]["body"])
        
	for section in json_dict[item]["article_dict"]['sections']:
            if 'canonical' in section:
		analyze_df.ix[article_id, 'article_name'] = section['name']
                if section['style'] != None:
                    article_section = section['style']
                else:
                    article_section = None
	analyze_df.ix[article_id, 'article_section'] = article_section
        if 'comments' in json_dict[item]["comment_dict"]:
	    analyze_df.ix[article_id, 'clicks'] = json_dict[item]["comment_dict"]["clicks"]
            for comment in json_dict[item]["comment_dict"]["comments"]:
                article_comment_count += 1
                
                user_id = json_dict[item]["comment_dict"]["comments"][comment]["author_id"]
                if user_id not in user_dict:
                    user_dict[user_id] = {}
                    user_dict[user_id]['article_id'] = []
                    user_dict[user_id]['comment_count'] = 0
                    user_dict[user_id]['reply_count'] = 0
                if json_dict[item]["comment_dict"]["comments"][comment]["has_reply"] == "yes":
                    user_dict[user_id]['reply_count'] += 1
                user_dict[user_id]['comment_count'] += 1
                user_dict[user_id]['article_id'].append(str(article_id))
                
                curr_comment_time_str = json_dict[item]["comment_dict"]["comments"][comment]["comment_ts"]
                curr_comment_time = datetime.datetime.strptime(curr_comment_time_str, '%B %d, %Y %H:%M:%S')
                
                comment_datetime_list.append(curr_comment_time)
                
                if 'comments_month_' + str(curr_comment_time.month) not in analyze_df:
                    analyze_df['comments_month_' + str(curr_comment_time.month)] = np.nan
                if math.isnan(analyze_df.ix[article_id, 'comments_month_' + str(curr_comment_time.month)]):
                    analyze_df.ix[article_id, 'comments_month_' + str(curr_comment_time.month)] = 0
                analyze_df.ix[article_id, 'comments_month_' + str(curr_comment_time.month)] += 1
                
                if 'comments_day_' + str(curr_comment_time.day) not in analyze_df:
                    analyze_df['comments_day_' + str(curr_comment_time.day)] = np.nan
                if math.isnan(analyze_df.ix[article_id, 'comments_day_' + str(curr_comment_time.day)]):
                    analyze_df.ix[article_id, 'comments_day_' + str(curr_comment_time.day)] = 0
                analyze_df.ix[article_id, 'comments_day_' + str(curr_comment_time.day)] += 1
                
                if 'comments_weekday_' + str(curr_comment_time.weekday()) not in analyze_df:
                    analyze_df['comments_weekday_' + str(curr_comment_time.weekday())] = np.nan
                if math.isnan(analyze_df.ix[article_id, 'comments_weekday_' + str(curr_comment_time.weekday())]):
                    analyze_df.ix[article_id, 'comments_weekday_' + str(curr_comment_time.weekday())] = 0
                analyze_df.ix[article_id, 'comments_weekday_' + str(curr_comment_time.weekday())] += 1
		
		if 'comments_hour_' + str(curr_comment_time.hour) not in analyze_df:
                    analyze_df['comments_hour_' + str(curr_comment_time.hour)] = np.nan
                if math.isnan(analyze_df.ix[article_id, 'comments_hour_' + str(curr_comment_time.hour)]):
                    analyze_df.ix[article_id, 'comments_hour_' + str(curr_comment_time.hour)] = 0
                analyze_df.ix[article_id, 'comments_hour_' + str(curr_comment_time.hour)] += 1
                
		if 'comments_year_' + str(curr_comment_time.year) not in analyze_df:
                    analyze_df['comments_year_' + str(curr_comment_time.year)] = np.nan
                if math.isnan(analyze_df.ix[article_id, 'comments_year_' + str(curr_comment_time.year)]):
                    analyze_df.ix[article_id, 'comments_year_' + str(curr_comment_time.year)] = 0
                analyze_df.ix[article_id, 'comments_year_' + str(curr_comment_time.year)] += 1
		
            analyze_df.ix[article_id, 'comment_count'] = article_comment_count
            
	    if comment_datetime_list != []:
		first_comment = min(comment_datetime_list)
		last_comment = max(comment_datetime_list)
		
		interval_first = first_comment - published_at
		interval_last = last_comment - published_at
		interval_first_last = last_comment - first_comment
		
		interval_first = divmod(interval_first.days * 86400 + interval_first.seconds, 60)[0]
		interval_last = divmod(interval_last.days * 86400 + interval_last.seconds, 60)[0]
		interval_first_last = divmod(interval_first_last.days * 86400 + interval_first_last.seconds, 60)[0]
		
		analyze_df.ix[article_id, 'interval_first'] = interval_first
		analyze_df.ix[article_id, 'interval_last'] = interval_last
		analyze_df.ix[article_id, 'interval_first_last'] = interval_first_last
    eta.done() 

with open('stats.csv', 'w') as csvfile:
    analyze_df.to_csv(csvfile, encoding='utf-8')

analyze_df = analyze_df[analyze_df['interval_first']>=0]

comments_df = analyze_df[analyze_df['comment_count']>0]

with open('stats_comments.csv', 'w') as csvfile:
    comments_df.to_csv(csvfile, encoding='utf-8')

for user_id in user_dict:
    user_df = user_df.append(pd.DataFrame({'user_id' : [user_id]}, index = [user_id]))
    user_df.ix[user_id, 'article_id'] = ','.join(user_dict[user_id]['article_id'])
    user_df.ix[user_id, 'comment_count'] = user_dict[user_id]['comment_count']
    user_df.ix[user_id, 'reply_count'] = user_dict[user_id]['reply_count']
    
with open('user_stats.csv', 'w') as csvfile:
    user_df.to_csv(csvfile, encoding='utf-8')