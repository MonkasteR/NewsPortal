from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter

from NewsPortal.settings import logger
from .models import Post


class NewsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name="dateCreation",
        lookup_expr="gt",
        widget=DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"type": "datetime-local"},
        ),
    )
    logger.info("Filter: NewsFilter")

    class Meta:
        model = Post
        fields = {
            "title": ["icontains"],
            "postCategory": ["exact"],
        }
