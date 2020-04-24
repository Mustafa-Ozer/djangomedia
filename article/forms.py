from django import forms
from .models import Article
from usersabout.models import usersAbout
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","content","article_image"]



class usersForm(forms.ModelForm):
    class Meta:
        model = usersAbout
        fields = ["about","phone","prof","links","pphoto"]
        