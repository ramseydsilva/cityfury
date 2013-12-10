from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.template import RequestContext
from fileupload.response import JSONResponse, response_mimetype
import json
from .serialize import serialize
from .forms import PostForm
from .models import *


def cities_data(request):
    cities = City.objects.filter(name__icontains=request.GET['term'])
    to_return = {'results': [], 'err': 'nil'}
    for city in cities:
        to_return['results'].append({'id': city.id, 'text': city.name})
    return HttpResponse(json.dumps(to_return), mimetype='application/json')

def areas_data(request):
    areas = Area.objects.filter(name__icontains=request.GET['term'])
    if request.GET['city']:
        try:
            areas = areas.filter(city__id=request.GET['city'])
        except:
            pass

    to_return = {'results': [], 'err': 'nil'}
    for area in areas:
        to_return['results'].append({'id': area.id, 'text': area.name})
    return HttpResponse(json.dumps(to_return), mimetype='application/json')

def post(request, error=False, message=""):

    if request.POST:
        caption = request.POST["caption"]
        description = request.POST["description"]
        category = request.POST["category"]
        city = request.POST["city"]
        area = request.POST.get("area", None)
        location = request.POST.get("location", "")
        image = request.FILES["image"]

        if caption == "":
            error = True
            message = "Please enter a caption"
        if category == "":
            error = True
            message = "Please enter a category"
        else:
            category = Category.objects.get(id=category)
        if city == "":
            error = True
            message = "Please enter a city"
        else:
            try:
                city = City.objects.get(id=city)
                city_created = False
            except:
                try:
                    city = City.objects.get(name__iexact=city)
                except:
                    city = City(name=city.capitalize())
                    city.save()
                    city_created = True

        if area != "":
            try:
                area = Area.objects.get(id=area, city=city)
            except:
                if area and not area.isdigit():
                    try:
                        area = Area.objects.get(name__iexact=area, city=city)
                    except:
                        area = Area(name=area.capitalize(), city=city)
                        area.save()

        if not image:
            error = True
            message = "Please select an image"

        if not error:
            post = Post(caption=caption, description=description, category=category, city=city, area=area, location_string=location, image=image)
            post.save()
            if not request.user.is_anonymous():
                post.user = request.user
                post.save()
            files = [serialize(post, file_attr="image")]
            data = {'files': files, 'post_url': post.get_absolute_url() }
            response = JSONResponse(data, mimetype=response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

    categories_json = []
    for category in Category.objects.all():
        categories_json.append({'id': category.id, 'text': category.name})

    context = {
        'cities': City.objects.all(),
        'categories': Category.objects.all(),
        'categories_json': json.dumps(categories_json),
        'message': message
    }

    return render_to_response("cityfury/post_form.html", context, context_instance = RequestContext(request))
