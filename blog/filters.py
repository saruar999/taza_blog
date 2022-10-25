import django_filters as filters
from django.db.models import Q, Count
from core.models import Posts

from django_filters.rest_framework import DjangoFilterBackend


class CustomFilterBackend(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        if request.user.is_anonymous:
            return PostsFilter(request.GET, queryset=queryset)
        classified_user = request.user.clasify_user()
        if classified_user == 'admin':
            return AdminPostsFilter(request.GET, queryset=queryset)
        else:
            return PostsFilter(request.GET, queryset=queryset)


class PostsFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_post')

    top_results_by = filters.CharFilter(method='get_top_results')

    author = filters.CharFilter(field_name='post_author__id', lookup_expr='exact')

    @staticmethod
    def get_top_results(queryset, name, value):
        if value == 'comments':
            return queryset.annotate(c_count=Count('comments')).order_by('-c_count',)
        elif value == 'likes':
            return queryset.order_by('-likes')[:10]
        else:
            return queryset

    @staticmethod
    def search_post(queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(body__icontains=value) | Q(tags__label__icontains=value)
        ).distinct()

    class Meta:
        model = Posts
        fields = ['title', 'body', 'tags']


class AdminPostsFilter(PostsFilter):

    sort = filters.CharFilter(method='get_sorted_qs')

    def get_sorted_qs(self, queryset, name, value):
        if value.startswith('-'):
            field = value[1:]
        else:
            field = value

        if getattr(self.Meta.model, field) is not None:
            return queryset.order_by(value)
        else:
            return queryset

