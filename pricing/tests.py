from django.test import TestCase
from django.shortcuts import render


# Create your tests here.

def index(request):
    context = {}
    return render(request, 'price_comparer', context)
