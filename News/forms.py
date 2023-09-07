from django import forms
from django.core.exceptions import ValidationError

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
        labels = {
            'author': 'Автор',
            'title': 'Заголовок',
            'text': 'Текст',
            'postCategory': 'Категория',
        }

    def clean(self):
        """
        Очищает введенные данные и убеждается, что описание не совпадает с заголовком.

        Возвращает:
            cleaned_data (dict): Очищенные введенные данные.

        Выбрасывает:
            ValidationError: Если описание совпадает с заголовком.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if text == title:
            raise ValidationError(
                "Описание не может совпадать с заголовком."
            )

        return cleaned_data
