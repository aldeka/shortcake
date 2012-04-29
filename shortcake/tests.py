from django.test import TestCase
from django.test.client import Client

from shortcake.models import Shurl, Domain, MonthLog, first_of_the_month
import datetime


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
class ShurlCreationTest(TestCase):
    def setUp(self):
        self.client = Client()
        s = Shurl(url='http://www.test.com')
        s.save()
        s.assign_short_suffix()
        
        # populate database with a lot of shurls
        i = 0
        while i < 66:
            url = 'http://www.testing.com/' + str(i) + '/'
            a = Shurl(url=url)
            a.save()
            a.assign_short_suffix()
            i += 1
        
    def test(self):
        s = Shurl.objects.get(pk=1)
        self.assertEqual(s.short_suffix,'1')
        self.assertEqual(s.access_count,0)
        
        another_s = Shurl.objects.get(pk=66)
        self.assertEqual(another_s.short_suffix,'12')
        
        yet_another_s = Shurl.objects.get(pk=63)
        self.assertEqual(yet_another_s.short_url(),'cak.es/_')
        
class Base64Test(TestCase):
    def test_shortening_algorithm(self):
        self.assertEqual('9',Shurl.shortening_algo(9))
        self.assertEqual('a',Shurl.shortening_algo(10))
        self.assertEqual('A',Shurl.shortening_algo(36))
        self.assertEqual('_',Shurl.shortening_algo(63))
        self.assertEqual('10',Shurl.shortening_algo(64))
        
class LoggingTest(TestCase):
    def setUp(self):
        self.client = Client()
        s = Shurl(url='http://www.test.com')
        s.save()
        s.assign_short_suffix()
        
        d = Domain.get_or_create(s.url)
        
        m = MonthLog(domain=d)
        m.save()
        
        past_time = datetime.date(2012,3,14)
        old_m = MonthLog(domain=d, creation_date=past_time, month=first_of_the_month(past_time))
        old_m.save()
        
    def test(self):
        s = Shurl.objects.latest()
        d = Domain.get_or_create(s.url)
        m = d.monthlog_set.get(month=first_of_the_month())
        old_m = d.monthlog_set.get(month=datetime.date(2012,3,1))
        
        self.assertEqual(0,s.access_count)
        self.assertEqual(0,d.access_count)
        self.assertEqual(0,m.access_count)
        
        url = s.get_url()
        # re-pull
        s = Shurl.objects.latest()
        m = d.monthlog_set.get(month=first_of_the_month())
        d = m.domain
        
        self.assertEqual(url,s.url)
        self.assertEqual(1,s.access_count)
        self.assertEqual(1,m.access_count)
        self.assertEqual(1,d.access_count)
        self.assertEqual(0,old_m.access_count)
        
class DomainTest(TestCase):
    def setUp(self):
        self.client = Client()
        s = Shurl(url='http://www.test.com/a/b/c/')
        s.save()
        s.assign_short_suffix()
        
        t = Shurl(url='http://www.test.com/another_dir/')
        t.save()
        t.assign_short_suffix()
        
        s.get_url()
        t.get_url()
        t.get_url()
        
    def test(self):
        s = Shurl.objects.get(pk=1)
        t = Shurl.objects.get(pk=2)
        self.assertEqual(s.access_count,1)
        self.assertEqual(t.access_count,2)
        
        self.assertEqual(Domain.extract_domain_from_url(s.url),'http://www.test.com')
        
        d = Domain.get_or_create(s.url)
        self.assertEqual(d.access_count,3)
