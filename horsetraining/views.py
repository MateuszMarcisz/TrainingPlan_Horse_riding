from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')


class TestView(View):
    def get(self, request):
        return render(request, 'horsetraining/test.html')
