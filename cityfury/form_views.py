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
        areas = areas.filter(city__id=request.GET['city'])

    to_return = {'results': [], 'err': 'nil'}
    for area in areas:
        to_return['results'].append({'id': area.id, 'text': area.name})
    return HttpResponse(json.dumps(to_return), mimetype='application/json')


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = "cityfury/post_form.html"

    def form_invalid(self, form):
        print self.request.POST
        return super(PostCreateView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object, file_attr="image")]
        data = {'files': files, 'post_url': self.object.get_absolute_url() }
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['cities'] = City.objects.all()
        categories = Category.objects.all()
        categories_json = []
        for category in categories:
            categories_json.append({'id': category.id, 'text': category.name})
        context['categories_json'] = json.dumps(categories_json)
        return context
