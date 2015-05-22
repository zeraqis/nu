#!/usr/bin/env python
import pandas as pd
import numpy as np
import math
from collections import OrderedDict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_dict(count_dict, fig_name, offset_label, xlabel, ylabel, labels):
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(1,1,1,)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)    
    
    ind = np.arange(len(count_dict))
    width = 0.4
    
    ax.set_title(fig_name)
    
    ax.bar(ind, count_dict.values(), width)
    
    ax.set_xticks(ind+width-0.1)
    
    if labels == []:
        for bin_count in count_dict.keys():
            labels.append(str(bin_count-offset_label) + '-' + str(bin_count))
    
    ax.set_xticklabels(labels, rotation=90)
    
    fig.savefig(fig_name + '.png')

with open('user_stats.csv', 'r') as csvfile:
    analyze_df = pd.DataFrame.from_csv(csvfile)

analyze_df['article_count'] = np.nan

for index, row in analyze_df.iterrows():
    analyze_df.ix[index, 'article_count'] = len(set(row['article_id'].split(',')))

print analyze_df['article_count'].describe()
print analyze_df['article_count'].median()
print analyze_df['article_count'].mode()

print analyze_df['comment_count'].describe()
print analyze_df['comment_count'].median()
print analyze_df['comment_count'].mode()

article_count_dict = {}
for count in analyze_df['article_count']:
    count_range_bin = int(math.ceil(count / 50.0)) * 50
    if count_range_bin not in article_count_dict:
        article_count_dict[count_range_bin] = 0
    article_count_dict[count_range_bin] += 1
ordered_article_count = OrderedDict(sorted(article_count_dict.items()))
plot_dict(ordered_article_count, 'user_article_count', 49, 'Unique Article Count Bin Ranges', 'No. of Users', [])

article_count_dict_100 = {}
for count in analyze_df['article_count']:
    if count <= 100:
        count_range_bin = count_range_bin = int(math.ceil(count / 5.0)) * 5
        if count_range_bin not in article_count_dict_100:
            article_count_dict_100[count_range_bin] = 0
        article_count_dict_100[count_range_bin] += 1
ordered_article_count_100 = OrderedDict(sorted(article_count_dict_100.items()))
plot_dict(ordered_article_count_100, 'user_article_count_100', 4, 'Article Count Bin Ranges', 'No. of Users', [])

comment_count_dict = {}
for count in analyze_df['comment_count']:
    count_range_bin = int(math.ceil(count / 100.0)) * 100
    if count_range_bin not in comment_count_dict:
        comment_count_dict[count_range_bin] = 0
    comment_count_dict[count_range_bin] += 1
ordered_comment_count = OrderedDict(sorted(comment_count_dict.items()))
plot_dict(ordered_comment_count, 'user_comment_count', 99, 'Comment Count Bin Ranges', 'No. of Users', [])

comment_count_dict_100 = {}
for count in analyze_df['comment_count']:
    if count <= 100:
        count_range_bin = count_range_bin = int(math.ceil(count / 5.0)) * 5
        if count_range_bin not in comment_count_dict_100:
            comment_count_dict_100[count_range_bin] = 0
        comment_count_dict_100[count_range_bin] += 1
ordered_comment_count_100 = OrderedDict(sorted(comment_count_dict_100.items()))
plot_dict(ordered_comment_count_100, 'user_comment_count_100', 4, 'Comment Count Bin Ranges', 'No. of Users', [])

with open('user_stats_count.csv', 'w') as csvfile:
    analyze_df.to_csv(csvfile, encoding='utf-8')