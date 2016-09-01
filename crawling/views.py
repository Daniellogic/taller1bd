from django.http import JsonResponse
from django.shortcuts import render
import json
import django_tables2 as tables
from django_tables2 import RequestConfig

from scrapyd_api import ScrapydAPI

import os.path

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
    scrapyd = ScrapydAPI('http://localhost:6800')
    
    filelatest = open("crawling/latest_run.txt", "r")
    scrapyd_jobid_latest = filelatest.read()
    filelatest.close()
    
    
    scrapyd_jobid = scrapyd_jobid_latest
    scrapyd_jobstatus = scrapyd.job_status('storeeventsscraper', scrapyd_jobid)
    
    
    if request.GET.get('new_run'):
        scrapyd_jobid = scrapyd.schedule('storeeventsscraper', 'uniandes')
        scrapyd_jobstatus = 'running'
        print("New run of scrapyd, with jobid:")
        print(scrapyd_jobid)
        filelatest = open("crawling/latest_run.txt", "w")
        filelatest.write(str(scrapyd_jobid))
        filelatest.close()
    if request.GET.get('check_status'):
        scrapyd_jobid = request.GET.get('check_status')
        scrapyd_jobstatus=scrapyd.job_status('storeeventsscraper', scrapyd_jobid)
        print("Checking status of scrapyd, with jobid:")
        print(scrapyd_jobid)
    if request.GET.get('cancel_run'):
        scrapyd_jobid = request.GET.get('cancel_run')
        scrapyd.cancel('storeeventsscraper',scrapyd_jobid)
        print("Cancelling scrapyd process, with jobid:")
        print(scrapyd_jobid)
    #scrapyd.cancel('storeeventsscraper','c900ba60705e11e68e2b0242ac112b50')
    #print("cancelled")
    
    
    current_directory = os.path.dirname(__file__)
    project_directory = os.path.split(current_directory)[0] # Repeat as needed
    env_directory = os.path.split(project_directory)[0] # Repeat as needed
    workspace_directory = os.path.split(env_directory)[0] # Repeat as needed
    print(current_directory)
    print(workspace_directory)
    
    
    events = []
    #for line in open('crawling/eventospipeline.json'):
    for line in open(workspace_directory + '/items/storeeventsscraper/uniandes/items/storeeventsscraper/uniandes/'+scrapyd_jobid_latest+'.jl'):
        try:
            events.append(json.loads(line))
        except:
            print("Error in json")
    #print(events)
    #events = events.filter(domain='http://ingenieria.uniandes.edu.co/')
    #print(events[1]['domain'])
    if request.GET.get('domainfilter'):
        events = [ event for event in events if request.GET.get('domainfilter') in event['domain'] ] # "http://ingenieria.uniandes.edu.co/"
    eventsTable = EventTable(events)
    RequestConfig(request).configure(eventsTable)
    return render(request, 'crawling.html', {'events': eventsTable, 'job_status': scrapyd_jobstatus,'job_id': scrapyd_jobid})#,{'job_status': scrapyd_jobstatus},{'job_id': scrapyd_jobid})
    #return JsonResponse(events, safe=False)
    #return render(request,"crawling.html")
    
