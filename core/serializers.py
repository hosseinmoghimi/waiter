from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from .models import BasicPage, Document, Image, PageComment, PageDocument, PageImage, PageLike, PageLink, Parameter, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields=['id','title','get_absolute_url']


class BasicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPage
        fields=['id','title','class_name_farsi','short_description','get_absolute_url','parent_id','thumbnail','short_description','get_edit_url']


class PageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageLink
        fields=['id','title','url','get_edit_url']


class PageDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageDocument
        fields=['id','title','get_download_url','get_edit_url','get_delete_url']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields=['id','title','get_download_url','get_edit_url','get_delete_url']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields=['id','name','app_name','value','get_edit_url','get_delete_url']


class PageLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageLike
        fields=['id','date_added']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields=['id','title','thumbnail','image','get_edit_url']


class PageImageSerializer(serializers.ModelSerializer):
    image=ImageSerializer()
    class Meta:
        model = PageImage
        fields=['id','image']


class PageCommentSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = PageComment
        fields=['id','comment','persian_date_added','profile']