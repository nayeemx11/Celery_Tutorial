# views.py
from django.shortcuts import render

from django.http import HttpResponse
from .tasks import add

def my_view(request):
    result = add.apply_async(args=[10, 20])  # Call task asynchronously
    return HttpResponse(f"Task result: {result.id}")
