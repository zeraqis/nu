import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import numpy as np
from collections import OrderedDict

def plot_dict(count_dict, fig_name, offset_label, xlabel, ylabel, labels=[]):
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

with open('stats.csv', 'r') as csvfile:
    analyze_df = pd.DataFrame.from_csv(csvfile)


publish_hours = analyze_df['published_hour']

publish_hour_dict = {}

for hour in publish_hours:
    if hour not in publish_hour_dict:
        publish_hour_dict[hour] = 0
    publish_hour_dict[hour] += 1

plot_dict(publish_hour_dict, 'published_all_hour', 0, 'Hour of the Day', 'Article Count', labels=range(0,24))


publish_weekday = analyze_df['published_weekday']

publish_weekday_dict = {}

for weekday in publish_weekday:
    if weekday not in publish_weekday_dict:
        publish_weekday_dict[weekday] = 0
    publish_weekday_dict[weekday] += 1

plot_dict(publish_weekday_dict, 'published_all_weekday', 0, 'Day of the Week', 'Article Count', labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

publish_months = analyze_df['published_month']

publish_month_dict = {}

for month in publish_months:
    if month not in publish_month_dict:
        publish_month_dict[month] = 0
    publish_month_dict[month] += 1

plot_dict(publish_month_dict, 'published_all_month', 0, 'Month of the Year', 'Article Count', labels=range(1,13))