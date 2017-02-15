from esp.program.models import ClassSubject
from esp.utils.web import render_to_response
from django.db.models.query import Q
from django.http import HttpResponse
import json

def good_random_class():
    return ClassSubject.objects.random_class(
            ~Q(parent_program__name__icontains='Delve') &
            ~Q(parent_program__name__icontains='SATPrep') &
            ~Q(parent_program__name__icontains='9001') &
            ~Q(parent_program__name__icontains='Test') &
            ~Q(title__iexact='Lunch Period')
            )

def main(request):
    return render_to_response("random/index.html", request,
        {'cls': good_random_class()})

def ajax(request):
    cls = good_random_class()
    data = {'title': cls.title,
            'program': cls.parent_program.niceName(),
            'info': cls.class_info,
            }
    return HttpResponse(json.dumps(data))
