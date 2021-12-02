from django.http import request
from .models import *
from .constants import *
from authentication.repo import ProfileRepo
from django.db.models import Q
from .enums import ParametersEnum
from authentication.repo import ProfileRepo
class TagRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=Tag.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for))
        return objects
    def tag(self,*args, **kwargs):
        pk=0
        if 'tag_id' in kwargs:
            pk=kwargs['tag_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        return self.objects.filter(pk=pk).first()
    
    def add_page_tag(self,*args, **kwargs):
        my_pages=BasicPageRepo(request=self.request).my_pages_ids()
        if self.user.has_perm(APP_NAME+".change_basicpage") or kwargs['page_id'] in my_pages:
            pass
        else:
            return None
        title=None
        page_id=None
        tag=None
        page=None
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        if 'title' in kwargs:
            title=kwargs['title']
        if title is not None:
            # tag=Tag.objects.get_or_create(title=title).tag
            tag=Tag.objects.filter(title=title).first()
            if tag is None:
                tag=Tag(title=title)
                tag.save()
        if page_id is not None:
            page=BasicPage.objects.filter(pk=page_id).first()

        if tag in page.tags.all():
            return None
        page.tags.add(tag)
        return tag
        
        

    def remove_page_tag(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_basicpage"):
            return None
        tag_id=None
        page_id=None
        tag=None
        page=None
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        if 'tag_id' in kwargs:
            tag_id=kwargs['tag_id']
        if tag_id is not None:
            # tag=Tag.objects.get_or_create(title=title).tag
            tag=Tag.objects.filter(pk=tag_id).first()
            if tag is None:
                return False
        if page_id is not None:
            page=BasicPage.objects.filter(pk=page_id).first()

        if page is None or not tag in page.tags.all():
            return False
        page.tags.remove(tag)
        return True
        
        
class BasicPageRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=BasicPage.objects
    def add_page(self,title,*args, **kwargs):
        new_page=BasicPage(title=title)
        new_page.title=title
        if 'parent_id' in kwargs:
            new_page.parent_id=kwargs['parent_id']
        new_page.save()
        new_page.app_name=new_page.parent.app_name
        new_page.class_name=new_page.parent.class_name
        new_page.save()
        return new_page
    def add_related_page(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_page"):
            return None
        page_id=0
        related_page_id=0
        bidirectional=True
        add_or_remove=True
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        if 'related_page_id' in kwargs:
            related_page_id=kwargs['related_page_id']
        if 'bidirectional' in kwargs:
            bidirectional=kwargs['bidirectional']
        if 'add_or_remove' in kwargs:
            add_or_remove=kwargs['add_or_remove']
        if add_or_remove is None:
            add_or_remove=True
        page=self.page(page_id=page_id)
        related_page=self.page(page_id=related_page_id)
        if page is None or related_page is None:
            return None
        if add_or_remove:
            page.related_pages.add(related_page)
            if bidirectional:
                related_page.related_pages.add(page)
            return related_page
        else:
            page.related_pages.remove(related_page)
            if bidirectional:
                related_page.related_pages.remove(page)
            return related_page


    def toggle_like(self,*args, **kwargs):
        page=self.page(*args, **kwargs)
        profile=ProfileRepo(request=self.request).me
        likes=PageLike.objects.filter(page=page).filter(profile=profile)
        if len(likes)==0 and profile is not None and page is not None:
            my_like=PageLike(page=page,profile=profile)
            my_like.save()
            return my_like
        else:
            likes.delete()
            return None
    
    def edit_page(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_basicpage"):
            return
        page=self.page(*args, **kwargs)
        if page is None:
            return
        if 'description' in kwargs and kwargs['description']  is not None and not kwargs['description'] == "" :
            page.description=kwargs['description']

        if 'short_description' in kwargs and kwargs['short_description']  is not None and not kwargs['short_description'] == "":
            page.short_description=kwargs['short_description']
        page.save()
        return page


    def edit(self,*args, **kwargs):
        return self.edit_page(*args, **kwargs)




    def page(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'page_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])        
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects.all()

    
    def my_pages_ids(self):
        pages_ids=[]
        if not self.request.user.is_authenticated:
            return []
        if self.request.user.has_perm('core.view_basicpage'):
            return BasicPage.objects.all()
        from projectmanager.repo import EmployeeRepo
        employee = EmployeeRepo(request=self.request).me
        if employee is not None:
            for project in employee.organization_unit.project_set.all():
                pages_ids.append(project.id)
        return pages_ids
        # return BasicPage.objects.filter(id__in=pages_ids)

    
class PageCommentRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageComment.objects
    def add_comment(self,comment,page_id,*args, **kwargs):
        profile=ProfileRepo(user=self.user).me
        page_comment=PageComment(comment=comment,page_id=page_id,profile=profile)
        
        page_comment.save()
        return page_comment

    def delete_comment(self,page_comment_id,*args, **kwargs):
        profile=ProfileRepo(user=self.user).me
        page_comment=PageComment.objects.filter(pk=page_comment_id).first()

        if page_comment is not None and page_comment.profile==profile:
            page_comment.delete()
            return True
        return False

    def page_link(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'page_link_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_link_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()


class NavLinkRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'app_name' in kwargs:
            app_name=kwargs['app_name']
            self.objects=NavLink.objects.filter(Q(app_name=app_name)).order_by("priority")
        else:
            self.objects=NavLink.objects.all().order_by("priority")
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'app_name' in kwargs:
            app_name=kwargs['app_name']
            objects=objects.filter(Q(app_name=app_name))
        return objects
    def nav_link(self,*args, **kwargs):
        pk=0
        if 'nav_link_id' in kwargs:
            pk=kwargs['nav_link_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        return self.objects.filter(pk=pk).first()
    

class PageLinkRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageLink.objects
        self.profile=ProfileRepo(request=self.request).me
    def add_page_link(self,title,url,*args, **kwargs):
        page=BasicPageRepo(request=self.request).page(*args, **kwargs)
        if page is not None:
            my_pages_ids=BasicPageRepo(request=self.request).my_pages_ids()
            
            if self.user.has_perm(APP_NAME+".add_pagelink") or page.id in my_pages_ids:
                pass
            else:
                return
        new_page_link=PageLink(title=title,page_id=page.id,url=url,icon_fa="fa fa-tag")
        new_page_link.new_tab=True
        new_page_link.save()
        return new_page_link

    def page_link(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'page_link_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_link_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()


class PageImageRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.profile=ProfileRepo(request=self.request).me
        self.objects=PageImage.objects
    def add_page_image(self,title,image,*args, **kwargs):
        
        page=BasicPageRepo(request=self.request).page(*args, **kwargs)
        if page is not None:
            my_pages_ids=BasicPageRepo(request=self.request).my_pages_ids()
            
            if self.user.has_perm(APP_NAME+".add_pagelink") or page.id in my_pages_ids:
                pass
            else:
                return
        
        image=Image(title=title,image_main_origin=image)
        image.save()
        new_page_image=PageImage(image=image,page_id=page.id)
        
        new_page_image.save()
        return new_page_image
    def delete_page_image(self,image_id,page_id,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".delete_pageimage"):
                
            pi=PageImage.objects.filter(image_id=image_id).filter(page_id=page_id)
            if len(pi)>0:
                pi.delete()
                if 'delete_image' in kwargs and kwargs['delete_image']:
                    Image.objects.filter(pk=image_id).delete()

                return True
  

class ParameterRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=Parameter.objects.filter(Q(app_name=None)|Q(app_name=self.app_name))
    
    def change_parameter(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+'.change_parameter'):
            return None
        parameter_id=kwargs['parameter_id'] if 'parameter_id' in kwargs else None
        parameter_name=kwargs['parameter_name'] if 'parameter_name' in kwargs else None
        parameter_value=kwargs['parameter_value'] if 'parameter_value' in kwargs else None
        app_name=kwargs['app_name'] if 'app_name' in kwargs else None
        if parameter_id is not None:
            parameter=Parameter.objects.filter(pk=parameter_id).first()
            if parameter is None:
                return None
        elif parameter_name is not None and app_name is not None:
            parameter=Parameter.objects.filter(app_name=app_name).filter(name=parameter_name).first()
            if parameter is None:
                parameter=Parameter(app_name=app_name,name=parameter_name,value_origin="")
                parameter.save()
        
        parameter.value_origin=parameter_value
        parameter.save()
        return parameter

    
    def set(self,name,value=None):
        # if name==ParametersEnum.LOCATION:
        #     value=value.replace('width="600"','width="100%"')
        #     value=value.replace('height="450"','height="400"') 
        if value is None:
            value=name
        olds=self.objects.filter(name=name).filter(app_name=self.app_name)
        if len(olds)>1:
            value=olds.first().value
        olds.delete()
        Parameter(name=name,value_origin=value,app_name=self.app_name).save()
    
    
    def parameter(self,*args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self,name):
        try:
            parameter=self.objects.filter(app_name=self.app_name).get(name=name)
        except:
            self.set(name=name)
            parameter=self.objects.filter(app_name=self.app_name).get(name=name)
        return parameter

    def list(self,*args, **kwargs):
        return self.objects.all()


class DocumentRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Document.objects.order_by('priority')

    def document(self,*args, **kwargs):
        
        if 'document_id' in kwargs:
            pk = kwargs['document_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_page_document(self,title,file,priority=1000,*args, **kwargs):
        
        page=BasicPageRepo(request=self.request).page(*args, **kwargs)
        if page is not None:
            my_pages_ids=BasicPageRepo(request=self.request).my_pages_ids()
            
            if self.user.has_perm(APP_NAME+".add_pagelink") or page.id in my_pages_ids:
                pass
            else:
                return
        

        document=PageDocument(icon_material="get_app",title=title,file=file,priority=priority,page=page,profile=self.profile)
        document.save()
        document.profiles.add(self.profile)
        return document


class PictureRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Picture.objects.all()
    def get(self,*args, **kwargs):
        pk=0
        name=""
        picture=None
        if 'name' in kwargs:
            name=kwargs['name']
            picture= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if picture is None and not name=="":
                picture=self.objects.create(app_name=self.app_name,name=name)
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        if pk>0:
            picture= self.objects.filter(app_name=self.app_name).filter(pk=pk).first()
        return picture

    def picture(self,*args, **kwargs):
        return self.get(*args, **kwargs)


class LinkRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Link.objects.all()
    def get(self,*args, **kwargs):
        pk=0
        name=""
        link=None
        if 'name' in kwargs:
            name=kwargs['name']
            link= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if link in None:
                link=self.objects.create(app_name=self.app_name,name=name)
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'link_id' in kwargs:
            pk=kwargs['link_id']
        if pk>0:
            link= self.objects.filter(app_name=self.app_name).filter(pk=pk).first()
        return link

