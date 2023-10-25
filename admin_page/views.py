from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def show_template(request):
    return HttpResponse("<h1>haha</h1>")