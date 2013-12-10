from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cityfury.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.template import Context
import json


def contact(request, contact_id, modal=False, template="cityfury/contact/contact_modal.html"):
    contact = get_object_or_404(Contact, id=contact_id)
    success = request.GET.get("success", False)

    modal = request.GET.get("modal", False)
    if modal:
        template = "cityfury/contact/contact_modal.html"

    context = {
        'contact': contact,
        'modal': modal,
        'success': success,
    }

    return render_to_response(template, context, context_instance = RequestContext(request))

def correct(request, contact_id, message="", success=False, template="cityfury/contact/correct_modal.html"):
    contact = get_object_or_404(Contact, id=contact_id)
    success = request.GET.get("success", False)

    if request.POST:
        name = request.POST["name"]
        title = request.POST["title"]
        website = request.POST["website"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        organisation = request.POST["organisation"]
        comments = request.POST["comments"]

        if int(bool(name) + bool(website) + bool(email) + bool(phone) + bool(organisation)) < 2:
            message = "Atleast two fields out of name, organisation, website, email or phone is mandatory"
        else:
            contact_correction = ContactCorrection(contact=contact, name=name, title=title, website=website, email=email, phone=phone, organisation=organisation, comments=comments)
            if not request.user.is_anonymous():
                contact_correction.added_by = request.user
            contact_correction.save()
            return redirect(reverse("contact_correct", args=[contact.id]) + "?modal=true&success=true")
    else:
        name = contact.name
        title = contact.title
        organisation = contact.organisation
        website = contact.website
        email = contact.email
        phone = contact.phone
        comments = ""

    context = {
        "edit": True,
        "name": name,
        "title": title,
        "organisation": organisation,
        "website": website,
        "email": email,
        "phone": phone,
        "comments": comments,
        "contact": contact,
        "message": message,
        "success": success,
    }

    return render_to_response(template, context, context_instance = RequestContext(request))

def resolve(request, message="", template="cityfury/contact/resolve_modal.html"):
    name = title = email = website = phone = organisation = comments = ""

    post = request.REQUEST.get("post", None)
    if post:
        post = get_object_or_404(Post, id=post)

    if request.POST:
        name = request.POST["name"]
        title = request.POST["title"]
        website = request.POST["website"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        organisation = request.POST["organisation"]
        comments = request.POST["comments"]

        if int(bool(name) + bool(website) + bool(email) + bool(phone) + bool(organisation)) < 2:
            message = "Atleast two fields out of name, organisation, website, email or phone is mandatory"
        else:
            contact = Contact(post=post, name=name, title=title, website=website, email=email, phone=phone, organisation=organisation, comments=comments)
            if not request.user.is_anonymous():
                contact.added_by = request.user
            contact.save()
            return redirect(reverse("contact", args=[contact.id]) + "?modal=true&success=true")

    context = {
        "add": True,
        "name": name,
        "title": title,
        "organisation": organisation,
        "website": website,
        "email": email,
        "phone": phone,
        "comments": comments,
        "post": post,
        "message": message,
    }
    return render_to_response(template, context, context_instance = RequestContext(request))

def view_corrections(request, contact_id, template="cityfury/contact/corrections_modal.html"):
    contact = get_object_or_404(Contact, id=contact_id)
    context = {
        "contact": contact
    }
    return render_to_response(template, context, context_instance = RequestContext(request))
