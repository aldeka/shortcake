#!/usr/bin/env python
# encoding: utf-8

import datetime

# this is bad and evil and what I'm using instead of a database, for now
# maps url strings to shurl objects
global_urls_table = dict()

class shurl():
    def __init__(self, url):
        self.url = url
        self.shurl = shorten_url_string(url)
        self.access_count = 0
        self.created_at = datetime.datetime.now()
        # dictionary mapping months (via datetime) to hits that month
        self.popularity_chart = dict((self.first_day_of_this_month(datetime.date.today()), 0))
        # add self to global table
        global_urls_table[url] = self
        
    @classmethod
    def first_day_of_this_month(date):
        return datetime.date(date.year, date.month, 1)
    
    def add_impression(self):
        '''Adds one to the impression count both globally and by month. You almost certainly want to use this method rather than updating the attributes directly!'''
        self.access_count += 1
        self.popularity_chart[first_day_of_this_month(datetime.date.today())] += 1

def shorten_url_string(url):
    '''Takes a url, returns shortened version'''
    # I'll probably have to change the root for testing purposes
    root = 'shrt.es/'
    return root + shortening_algo(url)
    
def shortening_algo(url):
    '''Takes a url, returns a unique identifier to be used in the shortened version'''
    count = len(global_urls_table)
    # TODO: convert this to string or something else clever
    return count
    
# *--*--*--*--*--*

# Get a URL, return shortened URL

def create_shortened_url(url):
    '''Returns existing short url if we've seen this url before, otherwise creates and returns a new one'''
    # check to see if we've seen this url before
    # TODO: More clever uniqueness checking, e.g. stripping off ? arguments or end /s
    if url in global_urls_table:
        return global_urls_table[url]
    s = shurl(url)
    return s.shurl

# Retrieve last 100 shortened urls

def last_100_urls():
    # sort and slice
    pass

# Retrieve top 10 most popular shortened urls in the last month
# I'm interpreting this as calendar months
# If you tracked impressions by day you could do it as "last 30 days" instead but that's more complicated

def popular_urls(date):
    # sort by popularity_chart[datetime.date(date.year, date.month, 1)], slice[:10]
    pass

# How many times a given shortened URL has been accessed
# shurl.access_count
