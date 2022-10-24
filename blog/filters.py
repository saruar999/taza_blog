import django_filters as filters
from django.db.models import Q
from core.models import Posts


class PostsFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_post')

    @staticmethod
    def search_post(queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(body__icontains=value) | Q(tags__label__icontains=value)
        ).distinct()

    class Meta:
        model = Posts
        fields = ['title', 'body', 'tags']