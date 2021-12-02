from django.urls import path
from . import apis,views
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name='home'),
    path("add_page/",apis.BasicApi().add_page,name='add_page'),
    path("add_page_document/",apis.BasicApi().add_page_document,name='add_page_document'),
    
    path("toggle_like/",apis.PageApi().toggle_like,name='toggle_like'),
    path("edit_page_description/",apis.PageApi().edit_page_description,name='edit_page_description'),
    path("change_parameter/",apis.BasicApi().change_parameter,name='change_parameter'),
    path("delete_page_comment/",apis.BasicApi().delete_page_comment,name='delete_page_comment'),
    path("add_page_comment/",apis.BasicApi().add_page_comment,name='add_page_comment'),
    path("delete_page_image/",apis.BasicApi().delete_page_image,name='delete_page_image'),
    path("add_page_image/",apis.BasicApi().add_page_image,name='add_page_image'),
    path("add_related_page/",apis.BasicApi().add_related_page,name='add_related_page'),
    path("add_page_tag/",apis.BasicApi().add_page_tag,name='add_page_tag'),
    path("remove_page_tag/",apis.BasicApi().remove_page_tag,name='remove_page_tag'),
    path("add_page_link",apis.BasicApi().add_page_link,name='add_page_link'),
    
    path("page/<int:pk>/",views.PageViews().page,name='page'),
    path("tag/<int:pk>/",views.PageViews().tag,name='tag'),
    path('page-chart/<int:pk>/',views.PageViews().page_chart,name="page_chart"),
    path("download/<int:pk>/",views.PageViews().download,name='download'),
]
