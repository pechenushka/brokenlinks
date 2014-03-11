from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    return HttpResponse('Hello World !')


def process(request):
    pass


def get_links(request):
    pass