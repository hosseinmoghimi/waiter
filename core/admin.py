from django.contrib import admin
from .models import BasicPage, Icon, Image, NavLink, PageComment, PageImage, PageLike, Parameter, Picture, SocialLink, Tag,Link,PageDocument,PageLink,Document

admin.site.register(Parameter)
admin.site.register(BasicPage)
admin.site.register(Icon)
admin.site.register(NavLink)
admin.site.register(PageLike)
admin.site.register(Picture)
admin.site.register(PageImage)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Document)
admin.site.register(PageLink)
admin.site.register(PageComment)
admin.site.register(PageDocument)
admin.site.register(SocialLink)