from django.contrib.auth import authenticate, login, logout
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django import forms
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User


def SuccessfulSignInRedirect(next, modal, request, close=False):
    modal_redirect_template = request.session.get("modal_redirect_template", "cityfury/includes/modal_close.html")
    if close and modal == "true":
        return render_to_response(modal_redirect_template, {}, context_instance = RequestContext(request))
    return HttpResponseRedirect(next)

def logout_view(request):
    l = logout(request)
    next = request.GET.get('next', reverse('home'))
    if not next:
        next = reverse('home')
    return HttpResponseRedirect(next)

def login_view(request, message='', username="", password="", template='cityfury/user/login.html', modal=False):
    modal = request.REQUEST.get("modal", False)
    close = request.REQUEST.get("close", False)
    if modal == "true":
        template = 'cityfury/user/login_modal.html'

    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse("home"))

    next = request.REQUEST.get('next', reverse('home'))

    if request.POST:
        username = request.POST['username']
        email_exists = User.objects.filter(email=username)
        if email_exists:
            username = email_exists[0].username

        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return SuccessfulSignInRedirect(next, modal, request, close=close)

        message = "Error logging you in, are you sure you're using the right credentials?"

    context ={'message' : message, 'next' : next, 'username': username, 'password': password, 'modal': modal, 'close': close }
    return render_to_response(template, context, context_instance = RequestContext(request))


def register_view(request, message='', username='', password='', email='', template='cityfury/user/register.html', modal=False):
    modal = request.REQUEST.get("modal", False)
    close = request.REQUEST.get("close", False)
    if modal == "true":
        template = 'cityfury/user/register_modal.html'

    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse("home"))

    next = request.REQUEST.get('next', reverse('home'))

    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

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
            return SuccessfulSignInRedirect(next, modal, request, close=close)

    context = {'next': next, 'message': message, 'username': username, 'password': password, 'email': email, 'modal': modal, 'close': close}
    return render_to_response(template, context, context_instance = RequestContext(request))

def get_login_buttons(request):
    next = request.REQUEST.get('next', reverse('home'))
    t = get_template('cityfury/includes/login_buttons.html')
    to_return = {
        "html": t.render(Context({'next': next, 'user': request.user }))
    }
    return HttpResponse(json.dumps(to_return), mimetype='application/json')
