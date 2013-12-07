from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cityfury.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.template import Context
import json


def get_posts(request):
    category = request.GET.get("category")
    city = request.GET.get("city")

    posts = Post.objects.all()
    paginator = Paginator(posts, 25)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    try:
        previous_page = posts.previous_page_number()
    except:
        previous_page = None

    try:
        next_page = posts.next_page_number()
    except:
        next_page = None

    t = get_template('cityfury/includes/ajax_posts.html')
    to_return = {
        "html": t.render(Context({"posts": posts})),
        "total_pages": posts.paginator.num_pages,
        "page": posts.number,
        "previous_page": previous_page,
        "next_page": next_page
    }

    return HttpResponse(json.dumps(to_return), mimetype='application/json')
