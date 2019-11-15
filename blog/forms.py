from django import forms
from .models import Post, Collection
from django.core.exceptions import ValidationError

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()  # .get('slug)

        if new_slug == 'create':
            raise ValidationError('Slug may not be create')
        return new_slug


class CityViewForm(forms.Form):
    city = forms.CharField(max_length=50)

    def clean_city(self):
        new_city = self.cleaned_data["city"]
        return new_city

class NewCreatePostForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.SlugField(max_length=150)
    body = forms.TextInput()

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'slug': forms.TextInput(attrs={'class': 'form-control'}),
        'body': forms.Textarea(attrs={'class': 'form-control'}),
        'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
    }


    def clean_slug(self):
        new_slug = self.cleaned_data["slug"]
        return new_slug


class CreateCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()  # .get('slug)

        if new_slug == 'create':
            raise ValidationError('Slug may not be create')
        return new_slug

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))