from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User


def logout_view(request):
    l = logout(request)
    next = request.GET.get('next', reverse('home'))
    return HttpResponseRedirect(next)


def login_view(request, message='', username="", password="", template='cityfury/user/login.html'):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse("home"))

    next = request.GET.get('next', reverse('home'))
    if request.POST:
        username = request.POST['username']
        email_exists = User.objects.filter(email=username)
        if email_exists:
            username = email_exists[0].username

        password = request.POST['password']

        next = request.POST.get('next', reverse('home'))
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(next)

        message = "Error logging you in, are you sure you're using the right credentials?"

    context ={'message' : message, 'next' : next, 'username': username, 'password': password }
    return render_to_response(template, context, context_instance = RequestContext(request))


def register_view(request, message='', username='', password='', email=''):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse("home"))

    next = request.GET.get('next', reverse('home'))
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        next = request.POST.get('next', reverse('home'))

        error = False

        if username == "":
            message = "Please enter a Username"
            error = True
        if not error and User.objects.filter(username=username):
            message = "That username has already been taken, please pick another one"
            error = True
        if not error and len(password) < 6:
            message = "Please enter a password of length greater than 5 characters"
            error = True
        try:
            validate_email(email)
        except forms.ValidationError:
            message = "Please enter a valid email address"
            error = True

        if not error:
            user = User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(next)

    context = {'next': next, 'message': message, 'username': username, 'password': password, 'email': email }
    return render_to_response('cityfury/user/register.html', context, context_instance = RequestContext(request))
