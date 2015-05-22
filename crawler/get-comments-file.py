import requests
from bs4 import BeautifulSoup
import re
import os
import json
from math import ceil


sub_dir = '/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nu/crawler/json_dumps/TNO_testdata_11_02_2015'
for root, dirs, files in os.walk(sub_dir):
	for filename in files:
		if '.article' in filename:
			file_dir = os.path.join(root, filename)
			with open(file_dir, 'r') as json_file:
				item = json.load(json_file)
				if item["social_counts"]["nujij_comments"] > 0:
					article_request = requests.get(item['url'])
					article_soup = BeautifulSoup(article_request.text, "html5lib")
					divs_social = article_soup.findAll('div', class_='socialbar-wrapper with-counters')
					
					for div in divs_social:
						a = div.find('li', class_="nujij").find('a', href=True)
						nujij_url = a['href']
					
					comment_pages = int(ceil(item["social_counts"]["nujij_comments"]/200.0))
					print comment_pages
					comment_urls = []
					comment_dict = {}
					comment_dict['comments'] = {}
					for i in range(comment_pages):
						if comment_urls == []:
							comment_request = requests.get(nujij_url)
							comment_urls.append(comment_request.url)
						else:
							comment_urls.append(comment_urls[0] + '?pageStart=' + str(i*200+1))
							comment_request = requests.get(comment_urls[i])
						print comment_request.status_code, comment_request.url, item['id']
						comment_soup = BeautifulSoup(comment_request.text, "html5lib")
						ol_reacties = comment_soup.find('ol', class_='reacties')
						if ol_reacties != None:
							li_reacties = comment_soup.find('ol', class_='reacties').findAll('li', class_='hidenum')
							comment_dict['url'] = list(comment_urls)
							comment_dict['article'] = item['id']
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
										regex = re.compile(r'[\n\r\t]')
										comment_dict['comments'][id_]['comment_body'] = regex.sub(' ', comment_text)
									img = li.find('img')
									anchor = img.findPrevious('a')
									split_anchor = anchor['href'].split('.')
									comment_dict['comments'][id_]['author_id'] = split_anchor[-2]
									#print comment_dict['comments'][id_]['author_id']
									comment_dict['comments'][id_]['author_url'] = anchor['href']
									comment_dict['comments'][id_]['author_img'] = img['src']
									comment_dict['comments'][id_]['author_name'] = img['alt']
							with open('json_dumps/TNO_testdata_11_02_2015/' + str(item['id']) + '.comment', 'w') as json_file:
									json.dump(comment_dict, json_file, indent = 4)