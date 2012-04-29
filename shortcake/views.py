from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext

from shortcake.models import Shurl, MonthLog, first_of_the_month, convert_from_base_64

from django.core import serializers
json_serializer=serializers.get_serializer("json")()

def home(request):
    '''TODO: This will have a form for submitting a URL to be shortened and handler for the POST thereof'''
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

    return render('index.html')
    
def latest(request,count):
    '''Returns the count'th most recent short urls'''
    response = json_serializer.serialize(Shurl.objects.all()[:count], ensure_ascii=False)
    return HttpResponse(response)
    
def top_ten(request):
    '''Return the 10 short urls with the most hits this month'''
    this_month_logs = MonthLog.objects.filter(month=first_of_the_month())
    popular_logs = this_month_logs.order_by('-access_count')[:10]
    shurls = []
    # this is kind of terrible, but whatev, it's only ten items
    for log in popular_logs:
        shurls.append(log.shurl)
    response = json_serializer.serialize(shurls, ensure_ascii=False)
    return HttpResponse(response)
    
def forward(request,short_suffix):
    '''Given the suffix of a short url, forwards us on to that short url's real url'''
    n = convert_from_base_64(short_suffix)
    shurl = get_object_or_404(Shurl,pk=n)
    return redirect(shurl.get_url())
    
def shurl_stats(request,short_suffix):
    '''Returns how many times a given short URL has been accessed'''
    n = convert_from_base_64(short_suffix)
    shurl = get_object_or_404(Shurl,pk=n)
    return HttpResponse('URL ' + short_suffix + ' has been accessed ' + shurl.access_count + ' time(s).')
