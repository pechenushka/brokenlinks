from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html', c)


def process(request):
    resource_types = request.POST.getlist('resource_types[]')
    resource_types = ['a'] if (len(resource_types) == 0) else resource_types

    c = {'site_url': request.POST['site_url']}
    c['resource_types'] = ', '.join(resource_types)

    return render_to_response('process.html', c)


def get_links(request):
    pass