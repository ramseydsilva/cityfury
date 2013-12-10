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

def posts(request):
    category = city = {'name': 'All'}

    posts = Post.objects.all()
    paginator = Paginator(posts, 50)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context = {
        'city': city,
        'category': category,
        'posts': posts,
        'open_category_nav': True,
        'open_city_nav': True,
    }

    return render_to_response("cityfury/post/posts.html", context, context_instance = RequestContext(request))

def category(request, category):
    if category == "all":
        return redirect("/")

    category = get_object_or_404(Category, name__iexact=category)

    posts = Post.objects.filter(category=category)
    paginator = Paginator(posts, 50)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    city = {'name': 'All'}

    context = {
        'city': city,
        'category': category,
        'posts': posts,
        'open_city_nav': True
    }
    return render_to_response("cityfury/post/city.html", context, context_instance = RequestContext(request))

def city(request, category, city):
    if city == "all":
        return redirect(reverse("category", args=[category]))

    city = get_object_or_404(City, name__iexact=city)
    posts = city.post_set.all()

    if category == "all":
        category = {'name': 'All'}
    else:
        category = get_object_or_404(Category, name__iexact=category)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 50)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'city': city,
        'category': category,
        'posts': posts
    }
    return render_to_response("cityfury/post/city.html", context, context_instance = RequestContext(request))

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.POST:
        comment = request.POST["comment"]
        if comment != "":
            comment = Comment(comment=comment, post=post)
            if not request.user.is_anonymous():
                comment.user = request.user
            comment.save()
        return redirect(reverse("post", args=[post.id]))

    context = {
        'post': post,
        'city': post.city,
        'category': post.category
    }
    return render_to_response("cityfury/post/post.html", context, context_instance = RequestContext(request))

def dislike(request, next=None, success=False, action=None):
    post = Post.objects.get(id=request.GET["post"])
    if request.user.is_anonymous():
        success = False
        next = request.get_full_path()
    else:
        dislike_exists = DisLike.objects.filter(user=request.user, post=post)
        if dislike_exists:
            dislike = dislike_exists[0]
            dislike.delete()
            action = "undisliked"
        else:
            dislike = DisLike(user=request.user, post=post)
            dislike.save()
            action = "disliked"
        success = True

    to_return = {
        'success': success,
        'action': action,
        'next': next,
        'dislikes': post.dislike_set.count()
    }
    return HttpResponse(json.dumps(to_return), mimetype='application/json')

def flag(request, post_id, success=False, template="cityfury/post/flag.html"):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_anonymous():
        return redirect(reverse("login") + "?modal=true&next=" + reverse("flag-post", args=[post.id]))

    if request.POST:
        comment = request.POST.get("comment", "")
        flag = PostFlag(comment=comment, user=request.user, post=post)
        flag.save()
        success = True

    context = {
        'post': post,
        'success': success
    }

    return render_to_response(template, context, context_instance = RequestContext(request))

