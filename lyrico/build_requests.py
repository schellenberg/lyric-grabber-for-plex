
from __future__ import print_function
from __future__ import unicode_literals

import copy
import random


user_agents = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36 OPR/35.0.2066.68',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
]

request_headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
	'DNT': '1',	
}

# randint inculdes both upper and lower bounds

def get_lyrico_headers(site_name=None):
	
	# Since each module requesting from different souce uses the same
	# request headers for a lyrico operation, make deep copies of base headers
	# before giving it to modules.

	headers_copy = copy.deepcopy(request_headers)
	headers_copy['User-Agent'] = user_agents[random.randint(0, (len(user_agents) - 1))]
	return headers_copy

def test_req_dic():
	print(request_headers)
