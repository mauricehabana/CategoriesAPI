import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.core import serializers
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from categories.models import Category


# Create your views here.

@csrf_exempt
def index(request):
    try:
        # if request.method == 'POST':
        received_json_data = json.loads(request.body.decode('utf-8'))
        if received_json_data is not None:
            Category.create_category(received_json_data)
            return HttpResponse('We are good')
    except:
        pass
    return Http404('We are Bad')


def detail(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    return JsonResponse(category.get_json())
