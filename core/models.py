
from django.core.files.storage import FileSystemStorage


from django.db import models, reset_queries
from django.db.models.base import Model
from django.db.models.fields import BooleanField, CharField
from .apps import APP_NAME
from django.utils.translation import deactivate, gettext as _
from .settings import *
from django.shortcuts import reverse
from django.http import Http404
from tinymce.models import HTMLField
from .enums import *
from utility.persian import PersianCalendar
IMAGE_FOLDER = APP_NAME+'/images/'

upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')
image = models.ImageField() 

class Icon(models.Model):
    name=models.CharField(_("name"), null=True,blank=True,max_length=50)
    icon_fa=models.CharField(_("fa"), null=True,blank=True,max_length=50)
    icon_material=models.CharField(_("material_icon"),null=True,blank=True, max_length=50)
    icon_svg=models.TextField(_("svg_icon"),null=True,blank=True)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    width = models.IntegerField(_("عرض آیکون"), null=True, blank=True)
    height = models.IntegerField(_("ارتفاع آیکون"), null=True, blank=True)
    image_origin = models.ImageField(_("تصویر آیکون"), upload_to=IMAGE_FOLDER+'Icon/',
                                     height_field=None, null=True, blank=True, width_field=None, max_length=None)
    
    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")

    def __str__(self):
        return self.name if self.name is not None else ("icon "+str(self.pk))

    def get_icon_tag(self, icon_style='', color=None,no_color=False):
        
        if color is not None:
            self.color = color
        text_color=''
        if not no_color and self.color is not None:
            text_color='text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="{text_color} material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{text_color} {self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'{self.icon_svg}'
        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''

    def get_icon_tag_pure(self, icon_style='', color=None,no_color=False):
        
        if color is not None:
            self.color = color
        text_color=''
        if not no_color and self.color is not None:
            text_color='text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="{text_color} material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{text_color} {self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''


class Tag(models.Model):
    priority = models.IntegerField(_("ترتیب"), default=100)
    title = models.CharField(_("عنوان"), max_length=50)
    icon=models.ForeignKey("Icon", verbose_name=_("icon"),null=True,blank=True, on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":tag", kwargs={"pk": self.pk})


class Image(models.Model):
    title = models.CharField(
        _("عنوان تصویر"), max_length=100, null=True, blank=True)
    description = models.CharField(
        _("شرح تصویر"), max_length=500, null=True, blank=True)
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Gallery/Photo/Thumbnail/',
                                         null=True, blank=True, height_field=None, width_field=None, max_length=None)
    image_main_origin = models.ImageField(_("تصویر اصلی"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Gallery/Photo/Main/', height_field=None, width_field=None, max_length=None)
    image_header_origin =models.ImageField(_("تصویر سربرگ"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Gallery/Photo/Header/', height_field=None, width_field=None, max_length=None)                              
   
    archive = models.BooleanField(_("بایگانی شود?"), default=False)
    priority = models.IntegerField(_("ترتیب"), default=100)
    location = models.CharField(
        _("موقعیت مکانی تصویر"), max_length=50, null=True, blank=True)
    profile = models.ForeignKey("authentication.profile", null=True,
                                blank=True, verbose_name=_("پروفایل"), on_delete=models.SET_NULL)

    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)
    def thumbnail(self):
        if(self.thumbnail_origin):
            return MEDIA_URL+str(self.thumbnail_origin)
        return self.image()

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/image/{self.pk}/change/"
    class Meta:
        verbose_name = _("GalleryPhoto")
        verbose_name_plural = _("تصاویر")
 
    def create_thumbnail(self,*args, **kwargs):
        #Opening the uploaded image
        if self.image_main_origin is None:
            return
        from PIL import Image as PilImage
        from io import BytesIO
        import sys
        from django.core.files.uploadedfile import InMemoryUploadedFile


        image = PilImage.open(self.image_main_origin)

        width11, height11= image.size
        ratio11=float(height11)/float(width11)

        output = BytesIO()
        from .repo import ParameterRepo
        THUMBNAIL_DIMENSION=ParameterRepo(app_name=APP_NAME).parameter(name="عرض تصاویر کوچک").value
        try:
            a=THUMBNAIL_DIMENSION+100
        except:
            THUMBNAIL_DIMENSION=250
        #Resize/modify the image
        image = image.resize( (THUMBNAIL_DIMENSION,int(ratio11*float(THUMBNAIL_DIMENSION))),PilImage.ANTIALIAS )
        
        #after modifications, save it to the output
        image.save(output, format='JPEG', quality=95)
        
        output.seek(0)
        

        #change the imagefield value to be the newley modifed image value
        image_name=f"{self.image_main_origin.name.split('.')[0]}.jpg"
        image_path=IMAGE_FOLDER+'image/jpeg'
        self.thumbnail_origin = InMemoryUploadedFile(output,'ImageField', image_name, image_path, sys.getsizeof(output), None)


    def save(self,*args, **kwargs):
        if not self.thumbnail_origin:
            self.create_thumbnail()
        return super(Image,self).save(*args, **kwargs)
    

    def get_absolute_url(self):
        return MEDIA_URL+str(self.image_main_origin)


class BasicPage(models.Model):
    title = models.CharField(_("عنوان"), max_length=300)
    sub_title=models.CharField(_("زیر عنوان"),null=True, blank=True, max_length=300)
    image_thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Page/Thumbnail/',
                                         null=True, blank=True, height_field=None, width_field=None, max_length=None)
    archive = models.BooleanField(_("بایگانی شود؟"), default=False)
    for_home=models.BooleanField(_("نمایش در خانه"),default=False)
    parent = models.ForeignKey("BasicPage",related_name="childs",null=True,blank=True, verbose_name=_(
        "والد"), on_delete=models.SET_NULL)
    icon = models.ForeignKey("icon", verbose_name=_(
        "icon"), null=True, blank=True, on_delete=models.CASCADE)
    panel = HTMLField(_("پنل"), null=True, blank=True)
    short_description = HTMLField(
        _("توضیح کوتاه"), null=True, blank=True)
    description = HTMLField(
        _("توضیح کامل"), null=True, blank=True)
    image_header_origin =models.ImageField(_("تصویر سربرگ"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Page/Header/', height_field=None, width_field=None, max_length=None)                              
    image_main_origin = models.ImageField(_("تصویر اصلی"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Page/Main/', height_field=None, width_field=None, max_length=None)
    
    
    priority = models.IntegerField(_('اولویت / ترتیب'), default=100)

    creator = models.ForeignKey("authentication.profile", verbose_name=_(
        "ایجاد شده توسط"), null=True, blank=True, on_delete=models.SET_NULL)

    status=models.CharField(_("status"),null=True,blank=True, max_length=50)
    color = models.CharField(_("رنگ"), blank=True, null=True,
                             choices=ColorEnum.choices, default=ColorEnum.PRIMARY, max_length=50)
    tags = models.ManyToManyField(
        "Tag", verbose_name=_("برچسب ها"), blank=True)
    meta_data=models.CharField(_("متا دیتا"),null=True,blank=True, max_length=100)
    app_name = models.CharField(_("نام اپ"),null=True,blank=True, max_length=50)
    class_name = models.CharField(_("نام کلاس"),null=True,blank=True, max_length=50)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    related_pages=models.ManyToManyField("BasicPage", blank=True,verbose_name=_("صفحات مرتبط"))
    keywords=models.CharField(_("keywords"),null=True,blank=True, max_length=50)
    @property
    def full_title(self,*args, **kwargs):
        seperator="/"
        if 'seperator' in kwargs:
            seperator=kwargs['seperator']
        if self.parent is not None:
            return self.parent.full_title+" "+seperator+" "+self.title
        return self.title
    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)
        images= self.pageimage_set.all()
        if len(images)>0:
            return images.first().image.image()
        elif len(self.pageimage_set.all())>0:
            return self.pageimage_set.all().first().image.image()

        return f'{STATIC_URL}{self.app_name}/img/pages/image/{self.class_name}.jpg'
    def image_header(self):
        if self.image_header_origin:
            return MEDIA_URL+str(self.image_header_origin)
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)
        if self.image_thumbnail_origin:
            return MEDIA_URL+str(self.image_thumbnail_origin)
        else:
            return f'{STATIC_URL}{self.app_name}/img/pages/header/{self.class_name}.jpg'
    def get_chart_url(self):
        return reverse(APP_NAME+':page_chart',kwargs={'pk':self.pk})
    
    def thumbnail(self):
        if self.image_thumbnail_origin:
            return MEDIA_URL+str(self.image_thumbnail_origin)
        elif self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)
        elif self.image_header_origin:
            return MEDIA_URL+str(self.image_header_origin)
        elif len(self.pageimage_set.all())>0:
            return self.pageimage_set.all().first().image.thumbnail()

        return f'{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png'
    def class_name_farsi(self):
        t=""
        if self.class_name=="project":
            t="پروژه"
        elif self.class_name=="blog":
            t="مقاله"
        elif self.class_name=="event":
            t="رویداد"
        elif self.class_name=="material":
            t="متریال"
        elif self.class_name=="service":
            t="سرویس"
        elif self.class_name=="organizationunit":
            t="واحد سازمانی"
        elif self.class_name=="employeespeciality":
            t="تخصص حرفه ای"
        elif self.class_name=="project":
            t="پروژه"
        return t
    def all_sub_pages(self):
        pages=[]
        pages.append(self)
        for page in BasicPage.objects.filter(parent=self):
            for page1 in page.all_sub_pages():
                pages.append(page1)
        return pages
    def get_breadcrumb_li(self):
        this_page_li= f"""
            <li class="breadcrumb-item">
            <a href="{self.get_absolute_url()}">{self.title}</a></li>
            """
        if self.parent is not None:
            return self.parent.get_breadcrumb_li()+this_page_li
        return this_page_li

    # def get_breadcrumb_li(self):
    #     if self.parent is None:
    #         home='<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':0})+'">خانه</a></li>'        
    #         return home+'<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':self.id})+'">'+self.name+'</a></li>'  
    #     else:
    #         return self.parent.get_breadcrumb_li()+self.get_breadcrumb_li()
    def get_breadcrumb(self):
        home_url=reverse(f'{self.app_name}:home')
        
        startnav="""<nav aria-label="breadcrumb">
            <ol class="breadcrumb mb-0" style="background:none !important;">
            """
        home=f"""
        <li class="breadcrumb-item">
            <a href="{home_url}">
                <i class="material-icons">home</i>
            </a>
        </li>"""
        inside=home+self.get_breadcrumb_li()         
        endnav='</ol></nav>'
        return startnav+inside+endnav

    class Meta:
        verbose_name = _("BasicPage")
        verbose_name_plural = _("BasicPages")

    def __str__(self):
        try:
            return f"{self.app_name}:{self.class_name}  {self.title}"
        except:
            return self.title
            # return "sdssdsdsdsdsd"

    def get_edit_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
        # return f"{ADMIN_URL}core/basicpage/{self.pk}/change/"
    def get_edit_btn(self):
        return f"""
        <a target="_blank" class="text-info" title="ویرایش {self.title}" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """
    def get_absolute_url(self):
        app_name=self.app_name
        class_name=self.class_name
        pk=self.pk
        return reverse(app_name+":"+self.class_name, kwargs={"pk": pk})
        # return reverse("core:page", kwargs={"pk": self.pk})

    def delete(self,*args, **kwargs):
        if 'delete_childs' in kwargs:
            for page in self.childs.all():
                page.delete()
        else:
            for page in BasicPage.objects.filter(parent=self):
                page.parent=self.parent
                page.save()
        return super(BasicPage,self).delete(*args, **kwargs)

    def images(self,*args, **kwargs):
        images=self.pageimage_set.all()
        ids=[]
        for image in images:
            ids.append(image.image.id)
        return Image.objects.filter(id__in=ids)

    def likes_count(self):
        return len(PageLike.objects.filter(page=self))

    def save(self,*args, **kwargs):
        return super(BasicPage,self).save()

    def documents_set(self):
        page_documents=self.pagedocument_set.all()
        ids=[]
        for pd in page_documents:
            ids.append(pd.document.id)
        documents= Document.objects.filter(id__in=ids).all()
        return documents


class Link(Icon):
    title = models.CharField(_("عنوان"), max_length=200)
    priority = models.IntegerField(_("ترتیب"), default=100)
    url = models.CharField(_("آدرس لینک"), max_length=2000, default="#")
    profile_adder = models.ForeignKey(
        "authentication.Profile", verbose_name=_("پروفایل"),null=True,blank=True, on_delete=models.CASCADE)
    new_tab=models.BooleanField(_('در صفحه جدید باز شود؟'),default=True)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    def persian_date_added_tag(self):
        value = self.date_added
        a = PersianCalendar().from_gregorian(value)
        return f"""
        <span  title="{value.strftime("%Y/%m/%d %H:%M:%S") }" class="text-secondary">
            <small>
                {str(a)}
            </small>   
        </span>
        """
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def persian_date_updated(self):
        return PersianCalendar().from_gregorian(self.date_updated)
    
    def get_link(self):
        return f"""

            <a target="_blank" href="{self.url}">
            {self.get_icon_tag()}
            <span class="mx-2">
            {self.title}
            </span>
            
            </a>
        """
    def get_link_btn(self):
        target='target="_blank"' if self.new_tab else ''
        return f"""

            <a {target} class="btn btn-{self.color} " href="{self.url}">
            <span class="ml-2">
            {self.get_icon_tag_pure()}
            </span>
            {self.title}
            </a>
        """

    def get_link_icon_tag(self):
        if self.url:
            icon = self.get_icon_tag()
            return f'<a title="{self.title}" href="{self.url}">{icon}</a>'
        else:
            return self.get_icon_tag()

    def to_link_tag(self):
        return """
          <a class="btn  btn-round btn-block btn-{color}" href="{url}">
         {icon}
          {title}</a>
        """.format(color=self.color, icon=self.get_icon_tag(), url=self.url, title=self.title)
    def target(self):
        if self.new_tab:
            return '_blank'
        # return '_parent'
        # return '_top'
        return '_self'
    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("لینک ها")

    def __str__(self):
        return self.title+'  ==> ' +self.url
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/link/{self.pk}/change/'
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" class="mx-2" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """

# class PageTag(models.Model):
#     page=models.ForeignKey("BasicPage", verbose_name=_("page"), on_delete=models.CASCADE)
#     keyword=models.CharField(_("KeyWord"), max_length=50)

#     class Meta:
#         verbose_name = _("PageTag")
#         verbose_name_plural = _("PageTags")

#     def __str__(self):
#         return f"{self.page.title} : {self.keyword}"

#     def get_absolute_url(self):
#         return reverse(APP_NAME+":tag", kwargs={"pk": self.pk})
class PageLike(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    page=models.ForeignKey("basicpage", verbose_name=_("page"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("PageLike")
        verbose_name_plural = _("PageLikes")

    def __str__(self):
        return self.page.title




class PageLink(Link):
    page=models.ForeignKey("BasicPage",related_name="links", verbose_name=_("page"),null=True,blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("لینک صفحات")
        verbose_name_plural = _("لینک های صفحات")

class Document(Icon):
    download_counter=models.IntegerField(_("تعداد دانلود"),default=0)
    title = models.CharField(_('عنوان'), max_length=200)
    priority = models.IntegerField(_('ترتیب'), default=100)
    profile = models.ForeignKey("authentication.Profile", verbose_name=_(
        "پروفایل"), on_delete=models.CASCADE)
    file = models.FileField(_("فایل ضمیمه"), null=True, blank=True,
                            upload_to=APP_NAME+'/documents', storage=upload_storage, max_length=100)
    mirror_link = models.CharField(_('آدرس بیرونی'),null=True,blank=True, max_length=10000)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    
    profiles=models.ManyToManyField("authentication.profile",blank=True,related_name="profile_documents", verbose_name=_("profiles"))
    is_open=models.BooleanField(_("is_open?"),default=False)
    def persian_date_added_tag(self):
        value = self.date_added
        a = PersianCalendar().from_gregorian(value)
        return f"""
        <span  title="{value.strftime("%Y/%m/%d %H:%M:%S") }" class="text-secondary">
            <small>
                {str(a)}
            </small>   
        </span>
        """
    
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/document/{self.pk}/change/'

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" class="mx-2" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def persian_date_updated(self):
        return PersianCalendar().from_gregorian(self.date_updated)
    def get_link(self):
        return f"""

            <a href="{self.get_download_url()}">
            {self.get_icon_tag()}
            {self.title}</a>
        """

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("اسناد")

    def get_download_url(self):
        if self.mirror_link and self.mirror_link is not None:
            return self.mirror_link
        if self.file:
            return reverse(APP_NAME+':download', kwargs={'pk': self.pk})
        else:
            return ''

    def download_response(self):
        #STATIC_ROOT2 = os.path.join(BASE_DIR, STATIC_ROOT)
        file_path = str(self.file.path)
        # return JsonResponse({'download:':str(file_path)})
        import os
        from django.http import HttpResponse
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                self.download_counter+=1
                self.save()
                return response
        raise Http404

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("dashboard:document", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/document/{self.pk}/change/'

    
    def get_delete_url(self):
        return f'{ADMIN_URL}{APP_NAME}/document/{self.pk}/delete/'

    
class PageDocument(Document):
    page=models.ForeignKey("BasicPage",related_name="documents", verbose_name=_("page"),null=True,blank=True, on_delete=models.CASCADE)
    

class PageComment(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    page=models.ForeignKey("basicpage", verbose_name=_("page"), on_delete=models.CASCADE)
    comment=HTMLField(verbose_name="comment")
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    
    class Meta:
        verbose_name = _("PageComment")
        verbose_name_plural = _("PageComments")


class Parameter(models.Model):
    app_name=models.CharField(_("app_name"),choices=AppNameEnum.choices,null=True,blank=True,max_length=20)
    name = models.CharField(_("نام"), max_length=50)
    value_origin = models.CharField(_("مقدار"),null=True,blank=True, max_length=10000)
    @property
    def value(self):
        if self.value_origin is None:
            return ''
        return self.value_origin
    @property
    def boolesan_value(self):
        if self.value_origin is None:
            return False
        if self.value_origin =='True':
            return True
        if self.value_origin =='1':
            return True
        if self.value_origin =='true':
            return True
        return False
    def get_edit_btn(self):
        return f"""
         <a target="_blank" title="ویرایش {self.name}" class="text-primary" 
         href="{self.get_edit_url()}">
                            <i class="material-icons"   aria-hidden="true" >edit</i>
                        </a>
        """

    class Meta:
        verbose_name = _("پارامتر")
        verbose_name_plural = _("پارامتر ها")

    def __str__(self):
        return f'{self.app_name} :{self.name} : {self.value_origin}'

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/change/'

    def get_delete_url(self):
        return f'{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/delete/'

    def save(self):
        if self.name==ParametersEnum.LOCATION:
            self.value_origin=self.value_origin.replace('width="600"','width="100%"')
            self.value_origin=self.value_origin.replace('height="450"','height="400"') 
        super(Parameter,self).save()


class PageImage(models.Model):
    page=models.ForeignKey("basicpage", verbose_name=_("page"),on_delete=models.CASCADE)
    image=models.ForeignKey("image", verbose_name=_("image"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("PageImage")
        verbose_name_plural = _("PageImages")

    def __str__(self):
        return f"{self.page.title} : {self.image.title}"

    def get_absolute_url(self):
        return reverse("PageImage_detail", kwargs={"pk": self.pk})


class Picture(models.Model):
    app_name=models.CharField(_("app_name"), max_length=50)
    name=models.CharField(_("name"), max_length=50)
    image_origin=models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"picture/", height_field=None, width_field=None, max_length=None)
    class_name="picture"
    
    def get_edit_btn(self):
        return f"""
            <a target="_blank" class="text-info farsi" title="ویرایش {self.name}" href="{self.get_edit_url()}">
            <i class="material-icons"   aria-hidden="true" >settings</i>
            ویرایش تصویر
            </a>
        """
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'


    def image(self):
        if self.image_origin and self.image_origin is not None:
            return f'{MEDIA_URL}{str(self.image_origin)}'
        return None

    class Meta:
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")

    def __str__(self):
        return self.app_name+" : "+self.name

    def get_absolute_url(self):
        return reverse("Picture_detail", kwargs={"pk": self.pk})


class SocialLink(Link):
    app_name=models.CharField(_('اپلیکیشن'),max_length=50,null=True,blank=True)
    profile = models.ForeignKey("authentication.Profile", null=True,
                                blank=True, verbose_name=_("profile"), on_delete=models.PROTECT)

    def get_link(self):
        return f"""
                <a href="{self.url}" class="btn btn-just-icon btn-link {self.icon_class}">
                {self.get_icon_tag()}
                </a>
        """

    class Meta:
        verbose_name = _("SocialLink")
        verbose_name_plural = _("شبکه اجتماعی")

    def __str__(self):
        return self.title


class NavLink(Link):
    app_name=models.CharField(_("app_name"),choices=AppNameEnum.choices, max_length=50)


    

    class Meta:
        verbose_name = _("NavLink")
        verbose_name_plural = _("NavLinks")
