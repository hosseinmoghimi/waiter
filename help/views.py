from django.conf.urls import url
from core.views import CoreContext
from .apps import APP_NAME
from django.shortcuts import render,reverse
from django.views import View
from phoenix.server_settings import apps
TEMPLATE_ROOT="help/"



def getContext(request):
    context = CoreContext(request=request, app_name=APP_NAME)    
    context['app']={
        'title':"راهنما",
        'home_url':reverse("help:home")
    }
    return context

def get_sidebar_links(app_name):
    sidebar_links=[]
    if app_name=='projectmanager':
        from projectmanager.help import sidebar_links
    if app_name=='farm':
        from farm.help import sidebar_links
    if app_name=='mafia':
        from mafia.help import sidebar_links
    if app_name=='messenger':
        from messenger.help import sidebar_links
    if app_name=='bms':
        from bms.help import sidebar_links
    if app_name=='realestate':
        from realestate.help import sidebar_links
    return sidebar_links

class HelpView(View):

    def index(self,request,*args, **kwargs):
        context=getContext(request=request)
        sidebar_index=[]
        for app in apps:
            if 'has_help' in app and app['has_help']:
                sidebar_index.append(app)

        context['sidebar_index']=sidebar_index
        return render(request,TEMPLATE_ROOT+"index.html",context)

    def app(self,request,app_name,*args, **kwargs):
        context=getContext(request=request)
        context['app_name']=app_name
        context['sidebar_links']=get_sidebar_links(app_name=app_name)
        return render(request,TEMPLATE_ROOT+"app.html",context)

    def help(self,request,app_name,template,*args, **kwargs):
        context=getContext(request=request)
        context['app_name']=app_name
        context['sidebar_links']=get_sidebar_links(app_name=app_name)
        return render(request,app_name+"/help/"+template+".html",context)

        
