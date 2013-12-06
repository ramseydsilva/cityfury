from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request):
    context = {}
    return render_to_response("home.html", context, context_instance = RequestContext(request))
