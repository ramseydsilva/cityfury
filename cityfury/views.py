from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cityfury.models import *


def home(request):
    context = {
        'home_page': True
    }
    return render_to_response("cityfury/home.html", context, context_instance = RequestContext(request))

def about(request):
    context = {
        'about_page': True
    }
    return render_to_response("cityfury/about.html", context, context_instance = RequestContext(request))

def contact(request):
    context = {
        'contact_page': True
    }
    return render_to_response("cityfury/contact.html", context, context_instance = RequestContext(request))

def support(request):
    context = {
        'support_page': True
    }
    return render_to_response("cityfury/support.html", context, context_instance = RequestContext(request))
