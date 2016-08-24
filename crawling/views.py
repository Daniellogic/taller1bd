from django.shortcuts import render

# Create your views here.

def homecrawling(request):  
    #return render_to_response("sumar.html", RequestContext(request))
    return render(request,"crawling.html")