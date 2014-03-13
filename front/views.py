from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.views.decorators.http import require_POST
from django.http.response import HttpResponse
from django.contrib import messages
import lxml.html
import json
import urllib
import re
from urlparse import urlparse
from mimetypes import guess_type

class JsonResponse(HttpResponse):
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
        super(JsonResponse, self).__init__(
            content=json.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type
        )


def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('front/index.html', c)


@require_POST
def process(request):
    resource_types = request.POST.getlist('resource_types[]')
    resource_types = ['a'] if (len(resource_types) == 0) else resource_types
    protocol = request.POST.get('protocol')
    url = request.POST.get('site_url')

    if url is None or len(re.findall(r'^[0-9a-zA-Z\-_/]*(?:\.[a-zA-Z]{,4})(?::\d+)?', url)) == 0:
        messages.error(request, 'Invalid arguments')
        return redirect('/')

    site_url = '%s://%s' % (protocol, url)

    c = dict()
    c['site_url'] = site_url
    c['resource_types'] = ', '.join(resource_types)

    return render_to_response('front/process.html', c)


def is_url_header_200(url):
    import urllib2
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'

    try:
        urllib2.urlopen(request)
        return True
    except urllib2.HTTPError:
        return False


def get_links(request):
    url = request.GET.get('url')
    resource_types = request.GET.getlist('resource_types')
    #uri = urlparse(url)

    result = []
    attribute_link_types = {
        'a': 'href',
        'script': 'src',
        'link': 'href',
        'img': 'src'
    }

    conn = urllib.urlopen(url)
    dom = lxml.html.fromstring(conn.read())
    conn.close()

    print resource_types

    for resource_type in resource_types:
        tag = resource_type
        href = attribute_link_types.get(tag)
        elements = dom.xpath('//%s/@%s' % (tag, href))

        for link in elements:
            resource_href = link

            if link.count('http') == 0:
                if link[0] is not '/':
                    resource_href = '{0}/{1}'.format(url, link)
                else:
                    resource_href = '{0}'.format(link)

            status = '200'
            is_file = False

            try:
                conn = urllib.urlopen(resource_href)
                status = conn.code
                is_file = guess_type(resource_href)[0] is not None
            except IOError as e:
                print e
            else:
                conn.close()

            result.append({
                'content': '',
                'href': resource_href,
                'type': tag,
                'status': status,
                'is_file': is_file
            })

    #html = urllib.urlopen(url).read()

    return JsonResponse(result)