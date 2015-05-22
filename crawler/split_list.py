#!/usr/bin/env python
import csv

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

article_list = []
with open('article_list-1.tsv', 'r') as listsfile:
    list_reader = csv.reader(listsfile, delimiter='\t')
    for row in list_reader:
        article_list.append(row[0])
article_lol = chunks(article_list, 3500)

for i, article_lol_item in enumerate(article_lol):
    with open('article_list_2013/list_' + str(i), 'w') as tsvfile:
        tsvwriter = csv.writer(tsvfile, delimiter='\t')
        for article in article_lol_item:
            tsvwriter.writerow([article])