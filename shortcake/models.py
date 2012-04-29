from django.db import models
from django.forms import ModelForm
import datetime
import string

optional = dict(blank=True, null=True)

def first_of_the_month(date=datetime.date.today()):
    return datetime.date(date.year, date.month, 1)
    
class Domain(models.Model):
    domain = models.URLField(unique=True)
    access_count = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.domain
    
    def get_or_create_log(self,month):
        ''' returns a MonthLog object, either old or freshly created, for the given first-of-the-month date '''
        try:
            log = self.monthlog_set.get(month=month)
        except DoesNotExist:
            log = MonthLog(domain=self,month=month)
            log.save()
        return log
    
    @staticmethod
    def extract_domain_from_url(url):
        ''' Takes a url, returns the url's domain '''
        # take apart the domain
        domain_parts = url.split('.')
        # get the tld out of the last period-separated chunk
        tail = domain_parts.pop()
        tail_parts = tail.split('/',1)
        tld = tail_parts[0]
        domain_parts.append(tld)
        # put the string back together
        return string.join(domain_parts, '.')
    
    @staticmethod
    def get_or_create(url):
        '''Returns a Domain object, either old or freshly created, based on a url'''
        domain = Domain.extract_domain_from_url(url)
        try:
            d = Domain.objects.get(domain=domain)
        except DoesNotExist:
            d = Domain(domain=domain)
            d.save()
        return d

class Shurl(models.Model):
    '''Model for a shortened URL.
    "No I'm not joking, and don't call me Shirley!"'''
    url = models.URLField(unique=True,verbose_name="URL")
    short_suffix = models.CharField(max_length=20,unique=True,**optional)
    access_count = models.IntegerField(default=0)
    creation_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.url
    
    class Meta:
        get_latest_by = 'creation_time'
        ordering = ['-creation_time']
    
    def short_url(self):
        '''Returns shortened version of url.'''
        # I'll probably have to change the shortener root for testing purposes
        root = 'cak.es/'
        return root + self.short_suffix
        
    def assign_short_suffix(self):
        '''Assigns shortener suffix to this short url. This should always be run after the shurl is first created and saved.'''
        self.short_suffix = Shurl.shortening_algo(self.pk)
        self.save()
        
    @staticmethod
    def shortening_algo(n):
        return convert_to_base_64(n)
    
    @staticmethod
    def is_nonunique(url):
        '''Tests to see if there's already a short url for this url. If so, returns the other object. If not, returns False'''
        # TODO: make this cleverer about duplicate-detection -- #s, ? arguments, www v. no www, etcetera
        # Even better: include function to identify common other url shortener services' urls, follow where they lead, and return the "real" url that they lead to. t.co, I'm looking at you...
        try:
            if url[-1] == '/':
                url = url[:len(url)-1]
            s = Shurl.objects.get(url='http://' + url + '/')
            return s
        except DoesNotExist:
            return False
    
    def get_url(self):
        '''Ups the access_count of the shurl, the shurl's domain, and the relevant month's log before returning the url. 
        You probably want to use this method instead of accessing the url directly!'''
        self.access_count += 1
        self.save()
        
        d = Domain.get_or_create(self.url)
        d.access_count += 1
        d.save()
        
        log = d.get_or_create_log(first_of_the_month())
        log.access_count += 1
        log.save()
        return self.url
        
class ShurlForm(ModelForm):
    class Meta:
        model=Shurl
        fields = ('url',)
        
class MonthLog(models.Model):
    '''Model for a log of accesses for a given domain in a given month.'''
    domain = models.ForeignKey(Domain)
    month = models.DateField(default=first_of_the_month())
    creation_date = models.DateField(auto_now_add=True)
    access_count = models.IntegerField(default=0)
        
    def __unicode__(self):
        return 'Log for ' + str(self.month) + ' of ' + self.domain.domain
        
    class Meta:
        ordering = ['month']
# -*-*-*-*-*- 

# Based on Greg Jorgenson's code snippet at http://code.activestate.com/recipes/65212/#c4

def convert_to_base_64(n):
    """convert positive decimal integer n to equivalent in base 64."""
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
    base = 64
    try:
        n = int(n)
    except:
        return ""
    if n < 0:
        return ""
    s = ""
    while 1:
        r = n % base
        s = digits[r] + s
        n = n / base
        if n == 0:
            break
    return s

def convert_from_base_64(s):
    """convert base 64 string to integer."""
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
    base = 64
    n = 0
    for char in s:
        n = n * base + string.index(digits,char)
    return n
