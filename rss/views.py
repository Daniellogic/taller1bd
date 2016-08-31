from django.shortcuts import render, redirect
from django.http import HttpResponse
from rss.rssform import RssForm
import simplexquery as sxq
import requests

# Create your views here.


def homerss(request):  
    #return render_to_response("sumar.html", RequestContext(request))
    feed = requests.get('http://www.huffingtonpost.es/feeds/verticals/spain/index.xml')
    #print(sxq.execute_all(".//rss//channel//item//title", feed.text))
    feedtitle = sxq.execute_all(".//rss//channel//item//title", feed.text)
    #return HttpResponse("<h1>titulos</h1>:" +  feed.text)
    #return HttpResponse(feedtitle, content_type='application/json')
    #feedtitle2 = feedtitle.rsplit('title', 1)[0]
    feedtitles = sxq.execute_all(".//rss/channel/item[position()=2]/title", feed.text)
    #return HttpResponse(feedtitles, content_type='application/json')
    return render(request,"rss.html")
 
def rssview(request):
    if request.method == 'POST':
        form = RssForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('rssviewss')
    else:
        form = RssForm()
    return render(request, 'rss.html', {'form':form})
    

def query(request):
    feed = requests.get('http://www.huffingtonpost.es/feeds/verticals/spain/index.xml')
    #try:
       
    #except:
        #return HttpResponse("Exception")
    queryatt = request.GET['queryrss']
    querytocomplete= "for $a in //rss/channel/item where ends-with($a/pubDate, '"+queryatt+"') return $a"
    #feedtitle = sxq.execute_all(".//rss/channel/item/[@title='"+queryatt+"']", feed.text)
    #feedtitle = sxq.execute_all(".//rss/channel/item/pubDate='Tue, 30 Aug 2016 15:09:43 -0400'", feed.text)
    feedtitle = sxq.execute_all(querytocomplete,feed.text)
    print(feedtitle)
    print("El request fue: " + queryatt)
    return HttpResponse(feedtitle, content_type='application/json')
    #return HttpResponse("Query OK " + queryatt)

