import requests
from bs4 import BeautifulSoup
import re
import os
import json
from math import ceil
import sys
import csv

regex = re.compile(r'[\n\r\t]')

#site = ' site:nujij.nl'

with open('crawl.log', 'w') as csvfile:
    log_writer = csv.writer(csvfile)
    with open('article_list_2014/list_' + str(sys.argv[1]), 'r') as list_file:
        list_reader = csv.reader(list_file, delimiter='\t')
        for row in list_reader:
            file_dir = 'json_dumps/crawls_2014/' + str(row[0]) + '.article'
            with open(file_dir, 'r') as json_file:
                item = json.load(json_file)
                status = ''
                while status != '200':
                    article_request = requests.get(item['url'])
                    print article_request.status_code, article_request.url
                    status = str(article_request.status_code)
                article_soup = BeautifulSoup(article_request.text, "html5lib")
                divs_social = article_soup.findAll('div', class_='socialbar-wrapper with-counters')
                for div in divs_social:
                    a = div.find('li', class_="nujij").find('a', href=True)
                    nujij_url = a['href']
                    actual_count = int(a.find('span', class_="counter").contents[0].strip())
                #if actual_count==0:
                #    query = item['title'] + site
                #    print query
                #    g = pygoogle(query)
                #    results = g.get_urls()
                #    print results
                #    for result in results[:10]:
                #        status=''
                #        while status != '200':
                #            comment_request = requests.get(result)
                #            status = str(comment_request.status_code)
                #        comment_soup = BeautifulSoup(comment_request.text, "html5lib")
                #        nu_url = comment_soup.find('div', class_='bericht-link').find('a')['href']
                #        nujij_article_id = nu_url.split('/')[4]
                #        if nujij_article_id == str(item['id']):
                #            print 'Found!'
                #            actual_count = int(regex.sub('',comment_soup.find('span', class_='bericht-reacties').contents[0].strip()))
                #            nujij_url = result
                #            break
                print 'comments : ', actual_count
                if actual_count > 0:
                    comment_pages = int(ceil(actual_count/200.0))
                    print 'pages : ', comment_pages
                    comment_urls = []
                    comment_dict = {}
                    comment_dict['comments'] = {}
                    comment_dict['sharer'] = {}
                    for i in range(comment_pages):
                        if i == 0:
                            #while str(nujij_article_id) != str(item['id']):
                            #    if nujij_article_id != '':
                            #        log_writer.writerow([item['id'], nujij_article_id, nu_url, article_request.url])
                            #        print item['id'], nujij_article_id, nu_url, article_request.url
                            status=''
                            while status != '200':
                                comment_request = requests.get(nujij_url)
                                status = str(comment_request.status_code)
                            actual_nujij_url = comment_request.url
                                #comment_soup = BeautifulSoup(comment_request.text, "html5lib")
                                #nu_anchor = comment_soup.find('div', class_='bericht-link').find('a')
                                #nu_url = nu_anchor['href']
                                #if nu_url!='':
                                #    nujij_article_id = nu_url.split('/')[4]
                                #else:
                                #    break
                        if comment_pages == 1:
                            comment_urls.append(actual_nujij_url)
                        if comment_pages > 1:
                            comment_urls.append(actual_nujij_url + '?pageStart=' + str(i*200+1))
                            status=''
                            while status != '200':
                                comment_request = requests.get(comment_urls[i])
                                status = str(article_request.status_code)
                        print comment_request.status_code, comment_request.url, item['id']
                        
                        comment_soup = BeautifulSoup(comment_request.text, "html5lib")
                        comment_dict['url'] = list(comment_urls)
                        comment_dict['article_id'] = str(item['id'])
                        clicks_str = regex.sub('',comment_soup.find('span', class_='bericht-clicks').contents[0].strip())
                        comment_dict['clicks'] = clicks_str.split()[0]
                        shared_by_div = comment_soup.find('div', class_='bericht-details')
                        comment_dict['sharer']['sharer_url'] = shared_by_div.find('a')['href']
                        comment_dict['sharer']['sharer_name'] = shared_by_div.find('img')['alt']
                        comment_dict['sharer']['sharer_img'] = shared_by_div.find('img')['src']
                        comment_dict['sharer']['shared_ts'] = shared_by_div.find('span')['publicationdate']
                        ol_reacties = comment_soup.find('ol', class_='reacties')
                        if ol_reacties != None:
                            li_reacties = comment_soup.find('ol', class_='reacties').findAll('li', class_='hidenum')
                            for li in li_reacties:
                                reactie_body = li.find('div', class_='reactie-body')
                                if reactie_body:
                                    id_ = li['id']
                                    #print id_
                                    if id_ not in comment_dict['comments']:
                                        comment_dict['comments'][id_] = {}
                                    comment_dict['comments'][id_]['comment_no'] = li.find('div', class_='reactie-nummer').contents[0]
                                    comment_dict['comments'][id_]['comment_votes'] =  []
                                    votes = li.findAll('div', class_='reactie-saldo')
                                    for vote in votes:
                                        comment_dict['comments'][id_]['comment_votes'].append(vote.contents[0])
                                    span_time = li.find('span', class_='tijdsverschil')
                                    comment_dict['comments'][id_]['comment_ts'] = span_time['publicationdate']
                                    comment_dict['comments'][id_]['has_reply'] = 'no'
                                    if reactie_body.find('span'):
                                        comment_dict['comments'][id_]['has_reply'] = 'yes'
                                        comment_dict['comments'][id_]['comment_body'] = {}
                                        comment_spans = reactie_body.findAll('span')
                                        replies = []
                                        for comment_span in comment_spans:
                                            replies.append(comment_span.contents[0])
                                        all_replies = [string for string in reactie_body(text=True) if string != '\n']
                                        #print all_replies, len(all_replies)
                                        for j, reply in enumerate(replies):
                                            if reply not in comment_dict['comments'][id_]['comment_body']:
                                                comment_dict['comments'][id_]['comment_body'][reply] = ''
                                            i = all_replies.index(reply)
                                            if j == 0 and i != 0 and len(all_replies) != 2 and all_replies[j].strip() !='':
                                                if 'None' not in comment_dict['comments'][id_]['comment_body']:
                                                    comment_dict['comments'][id_]['comment_body']['None'] = ''
                                                comment_dict['comments'][id_]['comment_body']['None'] = all_replies[j].strip()
                                            tmp_replies = all_replies.remove(reply)
                                            if i < len(all_replies):
                                                for reply_string in all_replies[i:]:
                                                    #print reply_string.encode('utf-8'), i
                                                    if tmp_replies != None:
                                                        if reply_string in tmp_replies:
                                                            break
                                                    comment_dict['comments'][id_]['comment_body'][reply] = comment_dict['comments'][id_]['comment_body'][reply] + ' ' + reply_string.strip()
                                                    comment_dict['comments'][id_]['comment_body'][reply] = comment_dict['comments'][id_]['comment_body'][reply].strip()
                                    else:
                                        comment_text = ' '.join(reactie_body(text=True)).strip()
                                        comment_dict['comments'][id_]['comment_body'] = regex.sub(' ', comment_text)
                                    img = li.find('img')
                                    anchor = img.findPrevious('a')
                                    split_anchor = anchor['href'].split('.')
                                    comment_dict['comments'][id_]['author_id'] = split_anchor[-2]
                                    #print comment_dict['comments'][id_]['author_id']
                                    comment_dict['comments'][id_]['author_url'] = anchor['href']
                                    comment_dict['comments'][id_]['author_img'] = img['src']
                                    comment_dict['comments'][id_]['author_name'] = img['alt']
                    with open('json_dumps/crawls_2014/' + str(item['id']) + '.comment', 'w') as json_file:
                        json.dump(comment_dict, json_file, indent = 4)