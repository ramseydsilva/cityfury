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

def contact(request, message=""):

    success = request.GET.get("success", False)
    name = email = comment = ""

    if request.POST:
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        comment = request.POST.get("comment", "")

        if not comment:
            message = "Please enter a comment."
        if not email:
            message = "Please enter your email address."
        if not name:
            message = "Please enter your name."

        if name and email and comment:
            contact_form = ContactForm(name=name, email=email, comment=comment)
            if not request.user.is_anonymous():
                contact_form.user = request.user
            contact_form.save()

            return redirect(reverse("contact") + "?success=true")

    context = {
        'contact_page': True,
        'success': success,
        'message': message,
        'name': name,
        'email': email,
        'comment': comment,
    }
    return render_to_response("cityfury/contact.html", context, context_instance = RequestContext(request))

def support(request):
    context = {
        'support_page': True
    }
    return render_to_response("cityfury/support.html", context, context_instance = RequestContext(request))
