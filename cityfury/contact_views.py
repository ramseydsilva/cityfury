from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cityfury.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.template import Context
import json


def contact(request, contact_id, modal=False, template="cityfury/contact/contact.html"):
    contact = get_object_or_404(Contact, id=contact_id)

    modal = request.GET.get("modal", False)
    if modal:
        template = "cityfury/contact/contact_modal.html"

    context = {
        'contact': contact,
        'modal': modal
    }

    return render_to_response(template, context, context_instance = RequestContext(request))
