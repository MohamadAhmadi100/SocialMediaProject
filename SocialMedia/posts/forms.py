from django.forms import ModelForm, Textarea
from .models import Post, Comment
from django.db import models


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': Textarea(
                attrs={'class': 'form-control col-md-8', 'placeholder': 'متن پست', 'rows': 6, 'cols': 80,
                       'style': 'resize:none;'}),
        }
        labels = {
            'body': '',
        }


class EditPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': Textarea(
                attrs={'class': 'form-control col-md-8', 'rows': 6, 'cols': 80,
                       'style': 'resize:none;'}),
        }
        labels = {
            'body': '',
        }


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': Textarea(
                attrs={'class': 'form-control col-md-8', 'placeholder': 'متن نظر', 'rows': 2, 'cols': 80,
                       'style': 'resize:none;'}),
        }
        labels = {
            'body': '',
        }


class AddReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': Textarea(
                attrs={'class': 'form-control col-md-8', 'placeholder': 'متن پاسخ', 'rows': 1, 'cols': 80,
                       'style': 'resize:none;'}),
        }
        labels = {
            'body': '',
        }
