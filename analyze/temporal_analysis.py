import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import numpy as np
from collections import OrderedDict

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

def plot_scatter(x_array, y_array, fig_name, xlabel, ylabel):
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(1,1,1,)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)    
    
    ax.set_title(fig_name)
    
    ax.scatter(x_array, y_array)
    
    fig.savefig(fig_name + '.png')

with open('stats_comments.csv', 'r') as csvfile:
    analyze_df = pd.DataFrame.from_csv(csvfile)

comment_count_dict = {}
print analyze_df['comment_count'].describe()
print 'comment_count sum : ', analyze_df['comment_count'].sum()
print 'comment_count mode : ', analyze_df['comment_count'].mode()
print 'comment_count median : ', analyze_df['comment_count'].median()
print 'comment_count var : ', analyze_df['comment_count'].var()
for count in analyze_df['comment_count']:
    count_range_bin = int(math.ceil(count / 100.0)) * 100
    if count_range_bin not in comment_count_dict:
        comment_count_dict[count_range_bin] = 0
    comment_count_dict[count_range_bin] += 1
ordered_comment_count = OrderedDict(sorted(comment_count_dict.items()))
plot_dict(ordered_comment_count, 'comment_count', 99, 'Comment Count Bin Ranges', 'No. of Articles', [])
plot_dict(ordered_comment_count, 'comment_count', 99, 'Comment Count Bin Ranges', 'No. of Articles', [])
del ordered_comment_count[100]
plot_dict(ordered_comment_count, 'comment_count_without_100', 99, 'Comment Count Bin Ranges', 'No. of Articles', [])
del ordered_comment_count[200]
plot_dict(ordered_comment_count, 'comment_count_without_100_200', 99, 'Comment Count Bin Ranges', 'No. of Articles', [])

comment_count_dict_100 = {}
for count in analyze_df['comment_count']:
    if count <= 100:
        count_range_bin = int(math.ceil(count / 10.0)) * 10
        if count_range_bin not in comment_count_dict_100:
            comment_count_dict_100[count_range_bin] = 0
        comment_count_dict_100[count_range_bin] += 1
small_comment_count_100 = OrderedDict(sorted(comment_count_dict_100.items()))
plot_dict(small_comment_count_100, 'comment_count_100', 9, 'Comment Count Bin Ranges', 'No. of Articles', [])

comment_count_dict_10 = {}
for count in analyze_df['comment_count']:
    if count <= 10:
        count_range_bin = count
        if count_range_bin not in comment_count_dict_10:
            comment_count_dict_10[count_range_bin] = 0
        comment_count_dict_10[count_range_bin] += 1
smaller_comment_count_10 = OrderedDict(sorted(comment_count_dict_10.items()))
plot_dict(smaller_comment_count_10, 'comment_count_10', 0, 'Comment Count Bin Ranges', 'No. of Articles', labels=range(1,11))


comment_hours = analyze_df.ix[:,'comments_hour_0':'comments_hour_9']
comment_hour_dict = {}
for hour in comment_hours:
    key_hour = int(hour.split('_')[2])
    comment_hour_dict[key_hour] = analyze_df[hour].sum()
plot_dict(comment_hour_dict, 'comment_hour', 0, 'Hour of the Day', 'Comment Count', labels=range(0,24))

publish_hours = analyze_df['published_hour']
publish_hour_dict = {}
for hour in publish_hours:
    if hour not in publish_hour_dict:
        publish_hour_dict[hour] = 0
    publish_hour_dict[hour] += 1
plot_dict(publish_hour_dict, 'published_hour', 0, 'Hour of the Day', 'Article Count', labels=range(0,24))


comment_weekday = analyze_df.ix[:,'comments_weekday_0':'comments_weekday_6']
comment_weekday_dict = {}
for weekday in comment_weekday:
    key_weekday = int(weekday.split('_')[2])
    comment_weekday_dict[key_weekday] = analyze_df[weekday].sum()
plot_dict(comment_weekday_dict, 'comment_weekday', 0, 'Day of the Week', 'Comment Count', labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

publish_weekday = analyze_df['published_weekday']
publish_weekday_dict = {}
for weekday in publish_weekday:
    if weekday not in publish_weekday_dict:
        publish_weekday_dict[weekday] = 0
    publish_weekday_dict[weekday] += 1
plot_dict(publish_weekday_dict, 'published_weekday', 0, 'Day of the Week', 'Article Count', labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])


comment_months = analyze_df.ix[:,'comments_month_1':'comments_month_9']
comment_month_dict = {}
for month in comment_months:
    key_month = int(month.split('_')[2])
    comment_month_dict[key_month] = analyze_df[month].sum()
plot_dict(comment_month_dict, 'comment_month', 0, 'Month of the Year', 'Comment Count', labels=range(1,13))

publish_months = analyze_df['published_month']
publish_month_dict = {}
for month in publish_months:
    if month not in publish_month_dict:
        publish_month_dict[month] = 0
    publish_month_dict[month] += 1
plot_dict(publish_month_dict, 'published_month', 0, 'Month of the Year', 'Article Count', labels=range(1,13))

print analyze_df['article_section'].value_counts()
print analyze_df['article_name'].value_counts()
article_sections_dict = {}
article_sections_comment_dict = {}
for index, row in analyze_df.iterrows():
    section = row['article_section']
    comment_count = row['comment_count']
    if section not in article_sections_dict:
        article_sections_dict[section] = 0
    if section not in article_sections_comment_dict:
        article_sections_comment_dict[section] = 0
    article_sections_dict[section] += 1
    article_sections_comment_dict[section] += comment_count
plot_dict(article_sections_dict, 'article_section', 0, 'Article Section', 'Article Count', labels=article_sections_dict.keys())
plot_dict(article_sections_comment_dict, 'article_section_comment', 0, 'Article Section', 'Comment Count', labels=article_sections_comment_dict.keys())

norm_interval_df = analyze_df[analyze_df['interval_first_last'] < 5000]

plot_scatter(np.array(norm_interval_df['interval_first_last']), np.array(norm_interval_df['comment_count']), 'comment_count_life_interaction', 'interval_first_last', 'comment_count')

plot_scatter(np.array(analyze_df['interval_first_last']), np.array(analyze_df['comment_count']), 'comment_count_life_interaction_outlier', 'interval_first_last', 'comment_count')

plot_scatter(np.array(analyze_df['article_length']), np.array(analyze_df['comment_count']), 'comment_count_length_interaction', 'article_length', 'comment_count')

print analyze_df.ix[:,'interval_first':'interval_last'].describe()
print analyze_df.ix[:,'interval_first':'interval_last'].mode()
print analyze_df.ix[:,'interval_first':'interval_last'].median()
print analyze_df.ix[:,'interval_first':'interval_last'].var()