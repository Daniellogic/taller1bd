from django.shortcuts import render, redirect
from django.http import HttpResponse
from rss.rssform import RssForm
import simplexquery as sxq
import requests
import re
from urllib import unquote

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
    queryatt = request.GET['queryrss']
    queryatt2 = request.GET['queryrss2']
    queryatt3 = request.GET['queryrss3']
    if queryatt != '': 
        querytocomplete = "for $x in //rss/channel/item return if ($x/pubDate[contains(., '"+queryatt+"')]) then <title>{data($x/title)}</title> else nothing"
        print("en el if: " + queryatt)
    else :
        if queryatt2 != '': 
            print("en el segundo if: " +queryatt2)
            querytocomplete = "for $x in //rss/channel/item return if ($x/link[contains(., '"+queryatt2+"')]) then <link>{data($x/link)}</link> else nothing"
        else :
            print("en el else: " +queryatt3)
            querytocomplete = "for $x in //rss/channel/item return if ($x/title[contains(., '"+queryatt3+"')]) then <title>{data($x/title)}</title> else nothing"
    
    ##querytocomplete= "for $x in //rss/channel/item return if ($x/pubDate[starts-with(., '"+queryatt+"')]) then <title>{data($x/title)}</title> else nothing"
    #querytocomplete= "for $a in //rss/channel/item/pubDate where ends-with($a, '"+queryatt+"') return $a"
    #querytocomplete= "for $a in //rss/channel/item where ends-with($a/pubDate, '"+queryatt+"') return $a"
    #feedtitle = sxq.execute_all(".//rss/channel/item/[@title='"+queryatt+"']", feed.text)
    #feedtitle = sxq.execute_all(".//rss/channel/item/pubDate='Tue, 30 Aug 2016 15:09:43 -0400'", feed.text)
    feedtitle = sxq.execute_all(querytocomplete,feed.text)
   
    print("El request fue: " +queryatt2)
    print("El request fue: " +queryatt3)
    return HttpResponse(feedtitle, content_type='application/json')
    #return HttpResponse("Query OK " + queryatt)

def query2(request):
    feed2 = requests.get('http://www.huffingtonpost.es/feeds/verticals/spain/index.xml')
    queryatt2 = request.GET['queryrss2']
    querytocomplete2 = "for $y in //rss/channel/item return if ($y/link[contains(., '"+queryatt2+"')]) then <title>{data($y/title)}</title> else nothing"
    feedtitle2 = sxq.execute_all(querytocomplete2,feed2.text)
    print("El request fue: " +queryatt2)
    return HttpResponse(feedtitle2, content_type='application/json')
    
def query3(request):
    feed3 = requests.get('http://www.huffingtonpost.es/feeds/verticals/spain/index.xml')
    queryatt3 = request.GET['queryrss3']
    querytocomplete3 = "for $z in //rss/channel/item return if ($z/title[contains(., '"+queryatt3+"')]) then <title>{data($z/title)}</title> else nothing"
    feedtitle3 = sxq.execute_all(querytocomplete3,feed3.text)
    print("El request fue: " +queryatt3)
    return HttpResponse(feedtitle3, content_type='application/json')
    
    
def regex(request):
    regex1 = requests.get('http://www.huffingtonpost.es/feeds/verticals/spain/index.xml')
    Dato = request.GET['regex']
    answer = re.compile('Dato{1,20}\s', re.IGNORECASE)
    totalanswer = re.findall()

    print("El request fue: " +queryatt2)
    return HttpResponse(feedtitle2, content_type='application/json')   