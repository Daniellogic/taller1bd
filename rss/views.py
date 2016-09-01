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
    datoregex = request.GET['regex']
    if queryatt != '': 
        querytocomplete = "for $x at $i in //rss/channel/item return if ($x/pubDate[contains(., '"+queryatt+"')]) then <title>{$i}. { ($x/pubDate) }{data($x/title)}{ ($x/description) }</title> else nothing"
        print("en el if: " + queryatt)
    else :
        if queryatt2 != '': 
            print("en el segundo if: " +queryatt2)
            querytocomplete = "for $x in //rss/channel/item return if ($x/link[contains(., '"+queryatt2+"')]) then <link>{data($x/link)}</link> else nothing"
        else :
            if queryatt3 != '':
                print("en el tercer if:" +queryatt3)
                querytocomplete = "for $x in //rss/channel/item return if ($x/title[contains(., '"+queryatt3+"')]) then <title>{data($x/title)}</title> else nothing"
                #feedtitle = sxq.execute_all(querytocomplete,feed.text)
                #return HttpResponse(feedtitle, content_type='application/json')
                print("fuera del if de:" +queryatt3)
            else :
                print("en el else final: " +datoregex)
                querytocomplete = re.compile(r'<link>(.*)</link>', re.IGNORECASE)
                totalanswer = re.findall(querytocomplete,feed.text)
    #mostrartitulo = sxq.execute(".//rss/channel/item/title", feed.text)
    #mostrardescripcion = sxq.execute_all(".//rss/channel/item/description", feed.text)
    #mostrarfechas = sxq.execute_all(".//rss/channel/item/pubDate", feed.text)
    #return HttpResponse(mostrartitulo, content_type='application/json')
    #return HttpResponse(mostrardescripcion, content_type='application/json')
    #return HttpResponse(mostrarfechas, content_type='application/json')
    feedtitle = sxq.execute_all(querytocomplete,feed.text)
    print("El request fue: " +queryatt2)
    print("El request fue: " +queryatt3)
    return HttpResponse(feedtitle, content_type='application/json')
    return HttpResponse(totalanswer, str(feed))
   
    
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
    answer = re.compile(r'<title>+' + re.escape(Dato) + r'</title>+', re.IGNORECASE)
    totalanswer = re.findall(answer,str(regex1))

    print(totalanswer)
    return HttpResponse(totalanswer)   