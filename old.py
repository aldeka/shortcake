#!/usr/bin/env python
# encoding: utf-8

import datetime

# this is bad and evil and what I'm using instead of a database, for now
# maps url strings to shurl objects
global_urls_table = dict()

class Shurl():
    def __init__(self, url):
        self.url = url
        self.shurl = shorten_url_string(url)
        self.access_count = 0
        self.creation_time = datetime.datetime.now()
        # add self to global table
        global_urls_table[url] = self
    
    def add_impression(self):
        '''Adds one to the impression count both globally and by month. You almost certainly want to use this method rather than updating the attributes directly!'''
        self.access_count += 1
        self.save()
        record = self.monthly_hits_record_set.get(month = monthly_hits_record.first_of_this_month()))
        record.access_count += 1
        record.save()
        
class Monthly_Hits_Record():
    def __init__(self, shurl):
        self.month = first_of_this_month()
        self.shurl = shurl
        self.access_count = 0
        
    @classmethod
    def first_of_this_month(date=datetime.date.today()):
        return datetime.date(date.year, date.month, 1)

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
    # Shurl.objects.all().order_by('-creation_time')[:100]
    pass

# Retrieve top 10 most popular shortened urls in the last month
# I'm interpreting this as calendar months
# If you tracked impressions by day you could do it as "last 30 days" instead but that's more complicated

def popular_urls(date):
    # sort by popularity_chart[datetime.date(date.year, date.month, 1)], slice[:10]
    # Shurl.objects.annotate(popularity_this_month=Count(monthly_hits_record_for_this_month.access_count)).order_by('-popularity_this_month')
    pass

# How many times a given shortened URL has been accessed
# shurl.access_count
