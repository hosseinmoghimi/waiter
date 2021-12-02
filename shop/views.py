from django.shortcuts import render
from django.views import View
from .apps import APP_NAME
from core.views import CoreContext

TEMPLATE_ROOT='shop/'


def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    LAYOUT_PARENT='phoenix/layout.html'
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)