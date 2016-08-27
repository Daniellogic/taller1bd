from django.shortcuts import render
from django.http import HttpResponse
import feedparser
import simplexquery as sxq
import requests

# Create your views here.

def homerss(request):  
    #return render_to_response("sumar.html", RequestContext(request))
    feed = requests.get('http://www.eltiempo.com/contenido/opinion/rss.xml')
    #feed = feedparser.parse('http://www.eltiempo.com/contenido/opinion/rss.xml')
    #print feed.text
    print(sxq.execute_all(".//title", feed.text))
    #print(sxq.execute("<html><body>{string(/COPYRIGHT)}</body></html>", feed))
    #print(sxq.execute("""<user>{"Taro"}</user>"""))
    return render(request,"rss.html")
    

def query(request):
    try:
        queryatt = request.GET['queryrss']
    except:
        return HttpResponse("Exception")
    print("El request fue: " + queryatt)
    return HttpResponse("Query OK " + queryatt)

