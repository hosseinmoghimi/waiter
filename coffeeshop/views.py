from django.shortcuts import render
from django.views import View
from .apps import APP_NAME

TEMPLATE_ROOT='coffeeshop/'
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context={}
        return render(request,TEMPLATE_ROOT+"index.html",context)