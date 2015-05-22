import json
import os
import pandas as pd
import numpy as np
import csv
from eta import ETA

sub_dir = '/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nu/crawler/json_dumps/crawls_2014/'
list_dir = '/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nu/crawler/article_list_2014/'
article_date_df = pd.DataFrame({'article' : [], 'date' : [] , 'section' : [], 'comment_count' : []})

#sections = {''}

eta = ETA(20)

for i in range(20):
	eta.print_status()
	with open(list_dir + 'list_' + str(i)) as list_file:
		list_reader = csv.reader(list_file, delimiter='\t')
		for row in list_reader:
			article_id = str(row[0])
			article_dir = sub_dir + row[0] + '.article'
			with open(article_dir, 'r') as article_file:
				article = json.load(article_file)
				article_id = article['id']
				if article["social_counts"]["nujij_comments"] > 0:
					comment_dir = sub_dir + row[0] + '.comment'
					with open(comment_dir, 'r') as comment_file:
						comment_dict = json.load(comment_file)
						comment_count = len(comment_dict['comments'])
				else:
					comment_count = 0
				flag = 0
				for i, section in enumerate(article['sections']):
					if 'canonical' in section:
						if section['style'] != None:
							article_date_df = article_date_df.append(pd.DataFrame({'article' : [str(article['id'])], 'date' : [article['published_at']], 'section' : [section['style']], 'comment_count' : [comment_count]}, index = [article_id]))
						else:
							article_date_df = article_date_df.append(pd.DataFrame({'article' : [str(article['id'])], 'date' : [article['published_at']], 'section' : [section['name']], 'comment_count' : [comment_count]}, index = [article_id]))
#article_date_df['section_counts'] = article_date_df.groupby(['section']).transform('count')
eta.done()
print article_date_df['section'].value_counts()
print article_date_df.shape
with open('section-count.csv', 'w') as csvfile:
	article_date_df.to_csv(csvfile, encoding='utf-8')