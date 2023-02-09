from django_filters import FilterSet, DateFilter
from django.forms import DateInput
from .models import Post


class PostFilter(FilterSet):
    time = DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateInput(
            format='%m-%d-%Y',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'category': ['exact'],
        }
