#!/usr/bin/env python
# encoding: utf-8
"""
delaware.py

Created by Matt Snider on 2010-05-07.
Copyright (c) 201. All rights reserved.
"""

import sys
import os
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup

def main():
	# Fetch S&P 500
	title = 'List_of_S%26P_500_companies'
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	infile = opener.open('http://en.wikipedia.org/w/index.php?title=%s' % title)
	html = infile.read()
	infile.close()
	soup = BeautifulSoup(html)
	tags = soup.findAll('tr')
	
	# Print out each company
	nDelaware = 0
	print 'Ticker, Company, State of Incorporation'
	for t in tags[1:]:
		symbol,company,secFiling = t.findAll('a')
		
		# Fetch SEC Filing: State of Incorporation
		fs = urlopen(secFiling['href'])
		html = fs.read()
		fs.close()
		m = re.search('<strong>([A-Z]*)</strong>', html)
		if (m):
			state = m.group(1)
		else:
			state = 'Private'
		
		if state == 'DE':
			nDelaware += 1

		print "%s, %s, %s" % (symbol.string,company.string,state)
	print '%d companies are incorporated in Delaware in the S&P 500' % nDelaware

if __name__ == '__main__':
	main()

