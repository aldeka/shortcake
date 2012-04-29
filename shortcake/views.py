from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext

from shortcake.models import Shurl, ShurlForm, MonthLog, first_of_the_month, convert_from_base_64

from django.core import serializers
json_serializer=serializers.get_serializer("json")()

def home(request):
    '''TODO: This will have a form for submitting a URL to be shortened and handler for the POST thereof'''
    if request.method == 'GET':
        form = ShurlForm()
        return render_to_response('index.html', {'form':form,}, context_instance=RequestContext(request))
    else:
        # handle post from form
        form = ShurlForm(request.POST)
        print request.POST['url']
        shurl = Shurl.is_nonunique(request.POST['url'])
        print shurl
        if not shurl:
            shurl = form.save()
            shurl.assign_short_suffix()
        return render_to_response('thanks.html', {'shurl':shurl,}, context_instance=RequestContext(request))

    return render('index.html')
    
def latest(request,count=100):
    '''Returns the count'th most recent short urls'''
    response = json_serializer.serialize(Shurl.objects.all()[:count], ensure_ascii=False)
    return HttpResponse(response)
    
def top_ten(request):
    '''Return the 10 domains with the most hits this month'''
    # note: if fewer than ten domains have had *any* hits this month, it may return fewer than ten
    this_month_logs = MonthLog.objects.filter(month=first_of_the_month())
    popular_logs = this_month_logs.order_by('-access_count')[:10]
    domains = []
    # this is kind of terrible, but whatev, it's only ten items
    for log in popular_logs:
        domains.append(log.domain)
    response = json_serializer.serialize(domains, ensure_ascii=False)
    return HttpResponse(response)
    
def forward(request,short_suffix):
    '''Given the suffix of a short url, forwards us on to that short url's real url'''
    n = convert_from_base_64(short_suffix)
    shurl = get_object_or_404(Shurl,pk=n)
    # get_url() updates the necessary access_counts and returns the url
    return redirect(shurl.get_url())
    
def shurl_stats(request,short_suffix):
    '''Returns how many times a given short URL has been accessed -- human readable'''
    n = convert_from_base_64(short_suffix)
    shurl = get_object_or_404(Shurl,pk=n)
    return HttpResponse('URL ' + short_suffix + ' has been accessed ' + str(shurl.access_count) + ' time(s).')
    
def shurl_accesses(request,short_suffix):
    '''Returns how many times a given short URL has been accessed'''
    n = convert_from_base_64(short_suffix)
    shurl = get_object_or_404(Shurl,pk=n)
    return HttpResponse(str(shurl.access_count))
    
def api_documentation(request):
    return HttpResponse('<h1>Welcome to the shortcake API!</h1> <ul> <li>popular/ --> Up to ten most popular (in terms of # of accesses) shortened domains this month. May return fewer than 10 if fewer than 10 domains have had any accesses!</li> <li>latest/ --> Last 100 shortened urls.</li> <li>latest/(n) --> Last n shortened urls.</li> <li>(shortener)/accesses/ --> How many times the given shortener has been accessed.</li></ul>')
