from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cityfury.models import *


def home(request):
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
        'open_city_nav': True,
        'open_category_nav': True
    }
    return render_to_response("home.html", context, context_instance = RequestContext(request))


def category(request, category):
    if category == "all":
        return redirect("/")

    category = get_object_or_404(Category, name__iexact=category)
    posts = Post.objects.filter(category=category)

    city = {'name': 'All'}

    context = {
        'city': city,
        'category': category,
        'posts': posts,
        'open_city_nav': True
    }
    return render_to_response("cityfury/city.html", context, context_instance = RequestContext(request))


def city(request, category, city):
    if city == "all":
        return reverse("category", args=[category])

    city = get_object_or_404(City, name__iexact=city)
    posts = city.post_set.all()

    if category == "all":
        category = {'name': 'All'}
    else:
        category = get_object_or_404(Category, name__iexact=category)
        posts = posts.filter(category=category)

    context = {
        'city': city,
        'category': category,
        'posts': posts
    }
    return render_to_response("cityfury/city.html", context, context_instance = RequestContext(request))


def post(request, post_id):
    post = Post.objects.get(id=post_id)

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
    return render_to_response("cityfury/post.html", context, context_instance = RequestContext(request))
