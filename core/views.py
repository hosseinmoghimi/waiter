import json
from core.serializers import DocumentSerializer,BasicPageSerializer, ImageSerializer, PageCommentSerializer, PageImageSerializer, PageLikeSerializer, PageLinkSerializer, TagSerializer
from django.utils import timezone
from django.shortcuts import render



from .apps import APP_NAME
from .forms import *
from .repo import *
from .settings import *
from .enums import *
from .utils import AdminUtility
from .constants import *
from django.views import View
TEMPLATE_ROOT = "core/"
from phoenix.server_settings import apps

def CoreContext(request, *args, **kwargs):
    context = {}
    app_name = 'core'
    context['wide_layout_parent']="phoenix/wide-layout.html"
    context['help_title']="راهنما"
    if 'app_name' in kwargs:
        app_name = kwargs['app_name']
    context['user'] = request.user
    context['apps']=apps
    profile= ProfileRepo(request=request).me
    context['profile'] =profile
    context['APP_NAME'] = app_name
    context['current_datetime'] = PersianCalendar(
    ).from_gregorian(timezone.now())
    context['current_date'] = PersianCalendar(
    ).from_gregorian(timezone.now())[:10]
    context[app_name+'_sidebar'] = True
    context['DEBUG'] = DEBUG
    context['ADMIN_URL'] = ADMIN_URL
    context['MEDIA_URL'] = MEDIA_URL
    context['SITE_URL'] = SITE_URL
    context['CURRENCY'] = CURRENCY
    context['PUSHER_IS_ENABLE'] = PUSHER_IS_ENABLE

    if PUSHER_IS_ENABLE and profile is not None and profile.member_set.first() is not None:
        from messenger.views import GetMemberContext
        from messenger.serializers import NotificationSerializer
        from messenger.repo import NotificationRepo
        context.update(GetMemberContext(request=request))
        notifications=NotificationRepo(request=request).list(member_id=context['member'].id,read=False)
        notifications_s=json.dumps(NotificationSerializer(notifications,many=True).data)
        context['notifications_s']=notifications_s
    else:
        context['PUSHER_IS_ENABLE'] = False
    return context


def PageContext(request, page):
    if page is None:
        raise Http404
    if page is None:
        return {}
    context = {}
    context['page'] = page

    context['parent_id'] = page.id
    from authentication.repo import ProfileRepo
    profile=ProfileRepo(request=request).me
    my_like=PageLike.objects.filter(page=page).filter(profile=profile).first()
    if my_like is None:
        my_like={'id':0}
    context['my_like'] =json.dumps(PageLikeSerializer(my_like).data)
    related_pages = page.related_pages.all()
    context['related_pages'] = related_pages
    context['related_pages_s'] = json.dumps(BasicPageSerializer(related_pages,many=True).data)
    my_pages_ids=BasicPageRepo(request=request).my_pages_ids()
    if request.user.has_perm(APP_NAME+".add_link") or page.id in my_pages_ids:
        context['add_page_link_form'] = AddPageLinkForm()
    if request.user.has_perm(APP_NAME+".change_page") or page.id in my_pages_ids:
        context['add_page_tag_form'] = AddPageTagForm()
        context['remove_page_tag_form'] = RemovePageTagForm()
    if ProfileRepo(request=request).me is not None:
        context['add_page_comment_form'] = AddPageCommentForm()

    if request.user.has_perm(APP_NAME+".add_document") or page.id in my_pages_ids:
        context['add_page_document_form'] = AddPageDocumentForm()

    if request.user.has_perm(APP_NAME+".add_pageimage") or page.id in my_pages_ids:
        context['add_page_image_form'] = AddPageImageForm()

    if request.user.has_perm(APP_NAME+".change_page"):
        context['add_related_page_form'] = AddRelatedPageForm()
        
    if request.user.has_perm(APP_NAME+".delete_pageimage"):
        context['delete_page_image_form'] = DeletePageImageForm()
    page_comments = page.pagecomment_set.all()
    context['documents_s'] = json.dumps(DocumentSerializer(page.documents.all(),many=True).data)
    context['page_comments'] = page_comments
    page_comments_s = json.dumps(
        PageCommentSerializer(page_comments, many=True).data)
    context['page_comments_s'] = page_comments_s
    context['page_tags']=page.tags.all()
    links=page.links.all()
    links_s=json.dumps(PageLinkSerializer(links,many=True).data)
    context['links_s']=links_s
    
    context['images_s']=json.dumps(ImageSerializer(page.images(),many=True).data)
    page_images=page.pageimage_set.all()
    # context['images_s']=json.dumps(PageImageSerializer(page_images,many=True).data)
    context['page_tags_s']=json.dumps(TagSerializer(page.tags.all(),many=True).data)
    if page.keywords is not None:
        context['keywords']=page.keywords



    return context


def getContext(request):
    context = DefaultContext(request=request, app_name=APP_NAME)
    context["layout_root"] = TEMPLATE_ROOT+"/layout.html"
    context["admin_utility"] = AdminUtility(request=request)
    return context
# Create your views here.


def DefaultContext(request, app_name='core', *args, **kwargs):
    context = CoreContext(request=request, app_name=app_name)
    return context


class MessageView(View):
    def __init__(self, *args, **kwargs):
        self.links = []
        self.message_text_html = None
        self.message_color = 'warning'
        self.has_home_link = True
        self.header_color = "rose"
        self.message_icon = ''
        self.header_icon = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        self.message_text = ""
        self.header_text = ""
        self.message_html = ""
        if 'message_html' in kwargs:
            self.message_html = kwargs['message_html']
        if 'message_color' in kwargs:
            self.message_color = kwargs['message_color']
        if 'has_home_link' in kwargs:
            self.has_home_link = kwargs['has_home_link']
        if 'header_color' in kwargs:
            self.header_color = kwargs['header_color']
        if 'message_icon' in kwargs:
            self.message_icon = kwargs['message_icon']
        if 'header_icon' in kwargs:
            self.header_icon = kwargs['header_icon']
        if 'message_text' in kwargs:
            self.message_text = kwargs['message_text']
        if 'header_text' in kwargs:
            self.header_text = kwargs['header_text']



    def response(self, request, *args, **kwargs):
        return self.show(request=request)

    def show(self, request, *args, **kwargs):
        context = CoreContext(request, *args, **kwargs)
        if self.header_text is None:
            self.header_text = 'خطا'
        if self.message_text is None:
            self.message_text = 'متاسفانه خطایی رخ داده است.'
        if self.has_home_link:
            btn_home = Link(url=(SITE_URL),
                            color=ColorEnum.SUCCESS+' btn-round',
                            icon_material=IconsEnum.home,
                            title='خانه', name='ssss', new_tab=False)
            self.links.append(btn_home)
        context['links'] = self.links

        context['header_text'] = self.header_text
        context['header_color'] = self.header_color
        context['header_icon'] = self.header_icon

        context['message_color'] = self.message_color
        context['message_icon'] = self.message_icon
        context['message_text'] = self.message_text
        context['message_html'] = self.message_html

        context['search_form'] = None
        return render(request, TEMPLATE_ROOT+'error.html', context)


class BasicViews(View):
    def home(self, request, *args, **kwargs):
        context = getContext(request)
        context['pages'] = BasicPageRepo(request=request).list(for_home=True)
        return render(request, TEMPLATE_ROOT+"index.html", context)


class PageViews(View):
    def page_chart(self, request, *args, **kwargs):
        context = getContext(request)
        if 'pk' in kwargs and kwargs['pk'] > 0:
            pk = kwargs['pk']
        else:
            pk = 0

        page = (BasicPageRepo(request=request).page(pk=pk))
        pages = page.all_sub_pages()
        pages_s = BasicPageSerializer(pages, many=True).data
        context['pages_s'] = json.dumps(pages_s)
        return render(request, "phoenix/pages-chart.html", context)

    def download(self, request, *args, **kwargs):
        me=ProfileRepo(request=request).me
        if me is None :
            raise Http404
        document = DocumentRepo(request=request).document(*args, **kwargs)
        if request.user.has_perm("core.change_document") or document.is_open or me in document.profiles.all():
            if document is None:
                raise Http404
            return document.download_response()

        # if self.access(request=request,*args, **kwargs) and document is not None:
        #     return document.download_response()
        message_view = MessageView()
        message_view.links = []
        message_view.links.append(Link(title='تلاش مجدد', color="warning",
                                  icon_material="apartment", url=document.get_download_url()))
        message_view.message_color = 'warning'
        message_view.has_home_link = True
        message_view.header_color = "rose"
        message_view.message_icon = ''
        message_view.header_icon = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        message_view.message_text = 'مجوز شما برای دسترسی به این صفحه مجاز نمی باشد.'
        message_view.header_text = 'دسترسی غیر مجاز'

        return message_view.response(request)

    def access(self, request, *args, **kwargs):
        document = DocumentRepo(request=request).document(pk=pk)
        self.me = ProfileRepo(request=request).me
        if self.me is not None and document.page in self.me.my_pages().all():
            return True
        if request.user.has_perm(APP_NAME+'.view_document'):
            return True
        if document.page.app_name == 'web':
            return True
        return False

    def page(self, request, *args, **kwargs):
        page = BasicPageRepo(request).page(*args, **kwargs)
        context = getContext(request)
        context['page'] = page
        context['add_child_form'] = AddPageForm()
        context['childs'] = page.childs.all()
        return render(request, TEMPLATE_ROOT+"page.html", context)

    def tag(self, request, *args, **kwargs):
        tag_repo=TagRepo(request=request)
        tag = tag_repo.tag(*args, **kwargs)
        context = getContext(request)
        pages=tag.basicpage_set.all()
        context['tag'] = tag
        context['pages'] = pages
        context['pretitle'] = "صفحات دارای برچسب " 
        context['title'] =  tag.title
        context['subtitle2'] = "صفحات دارای برچسب "+tag.title
        return render(request, TEMPLATE_ROOT+"pages.html", context)
