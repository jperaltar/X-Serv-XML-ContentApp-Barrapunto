from django.shortcuts import render
from models import Pages, News
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
import xmlparser
from datetime import datetime, date, time, timedelta

# Create your views here.

last = datetime.now()

@csrf_exempt
def main(request, resource):
    deltatime = timedelta(0, 5*60, 0)

    if request.method == "GET":
        try:
            now = datetime.now()
            if (now - last) > deltatime:
                print "Updating..."
                content = xmlparser.getNews()
                news = News.objects.create(html=content)
                news.save()

            page_entry = Pages.objects.get(name=resource)
            try:
                news = News.objects.get(id=1)
            except News.DoesNotExist:
                print "Updating..."
                content = xmlparser.getNews()
                news = News.objects.create(html=content)
                news.save()

            output = page_entry.page + "</br>\n" + news.html
            return HttpResponse(output)
        except Pages.DoesNotExist:
            return HttpResponseNotFound(
                'Page not found: /%s.' % resource)
    elif request.method == "PUT":
        new_entry = Page(name=resource, page=request.body)
        new_entry.save()
        return HttpResponse("Succesful PUT operation: " 
                            + request.body)
    else:
        return HttpResponseForbidden("Operation not available")
