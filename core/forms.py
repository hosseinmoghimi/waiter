from django import forms

class AddPageForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=100, required=True)
    
class EditPageDescriptionForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    description=forms.CharField(required=False,max_length=1000)
    short_description=forms.CharField(required=False,max_length=1000)
    

class DeletePageImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    image_id=forms.IntegerField(required=True)
    
class PageLikeToggleForm(forms.Form):
    page_id=forms.IntegerField(required=True)

    
class AddRelatedPageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    related_page_id=forms.IntegerField(required=True)
    bidirectional=forms.BooleanField(required=False)
    add_or_remove=forms.BooleanField(required=False)

class ChangeParameterForm(forms.Form):
    parameter_id=forms.IntegerField(required=False)
    app_name=forms.CharField(max_length=50,required=False)
    parameter_name=forms.CharField(max_length=100,required=False)
    parameter_value=forms.CharField(max_length=10000,required=True)

class AddPageTagForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=True)


class RemovePageTagForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    tag_id=forms.IntegerField(required=True)


class AddPageLinkForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    url=forms.CharField(max_length=1000, required=True)
    

class AddPageDocumentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    

class AddPageImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    

class AddPageCommentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    comment=forms.CharField(max_length=500, required=True)
    

class DeletePageCommentForm(forms.Form):
    page_comment_id=forms.IntegerField(required=True)