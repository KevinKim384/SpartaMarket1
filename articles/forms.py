from .models import Article
from django import forms

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),}
class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),}
        exclude = ('likes',)