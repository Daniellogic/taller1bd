from django.http import JsonResponse
from django.shortcuts import render
import json
import django_tables2 as tables
from django_tables2 import RequestConfig

from django.core import serializers

# Create your views here.

class EventTable(tables.Table):
    domain = tables.Column()
    title = tables.Column()
    dates = tables.Column()
    desc = tables.Column()
    owner = tables.Column()
    

def homecrawling(request):  
    #return render_to_response("sumar.html", RequestContext(request))
    events = []
    for line in open('crawling/eventospipeline.json'):
        events.append(json.loads(line))
    #print(events)
    #events = events.filter(domain='http://ingenieria.uniandes.edu.co/')
    #print(events[1]['domain'])
    if request.GET.get('domainfilter'):
        events = [ event for event in events if request.GET.get('domainfilter') in event['domain'] ] # "http://ingenieria.uniandes.edu.co/"
    eventsTable = EventTable(events)
    RequestConfig(request).configure(eventsTable)
    return render(request, 'crawling.html', {'events': eventsTable})
    #return JsonResponse(events, safe=False)
    #return render(request,"crawling.html")
    
