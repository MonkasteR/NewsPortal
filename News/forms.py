from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Post


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=128)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'postCategory',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if text == title:
            raise ValidationError(
                "Описание не может совпадать с заголовком."
            )

        return cleaned_data


class ArticleForm(CreateView):
    title = forms.CharField(max_length=128)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'postCategory',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if text == title:
            raise ValidationError(
                "Описание не может совпадать с заголовком."
            )

        return cleaned_data

    def form_valid(self, form):
        categoryType = form.save(commit=False)
        categoryType.choices = NEWS
        return super().form_valid(form)
