from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #return HttpResponse("Hello World!!")
    return render(request, '../../../Front-end/index.html')

# Create your views here.
