from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homerss(request):  
    #return render_to_response("sumar.html", RequestContext(request))
    return render(request,"rss.html")
    
def query(request):
    try:
        queryatt = request.GET['queryrss']
    except:
        return HttpResponse("Exception")
    print("El request fue: " + queryatt)
    return HttpResponse("Query OK " + queryatt)