import json
import datetime
import time
import pandas as pd
import math
import numpy as np

analyze_df = pd.DataFrame()
analyze_df['published_at'] = []
article_id = 123
article_comment_count = 0

pub_list = ["2014-02-03T14:10:08", "2014-02-04T14:10:08", "2014-02-15T14:10:08"]



for published_at_str in pub_list:
    published_at = datetime.datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%S')
    analyze_df = analyze_df.append(pd.DataFrame({'published_at' : [published_at]}, index = [article_id]))
    
    if 'published_month' not in analyze_df:
        analyze_df['published_month'] = np.nan
    analyze_df.ix[article_id, 'published_month'] = published_at.month
    
    if 'published_day' not in analyze_df:
        analyze_df['published_day'] = np.nan
    analyze_df.ix[article_id, 'published_day'] = published_at.day
    
    if 'published_weekday' not in analyze_df:
        analyze_df['published_weekday'] = np.nan
    analyze_df.ix[article_id, 'published_weekday'] = published_at.weekday()

print analyze_df