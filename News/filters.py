from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter

from .models import Post


class NewsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    # postCategory = CharFilter(
    #     field_name='postCategory',
    #     lookup_expr='icontains',
    # )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'postCategory': ['exact'],
        }
