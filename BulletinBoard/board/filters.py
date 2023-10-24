from django_filters import FilterSet, CharFilter
from .models import Comment


class CommentFilter(FilterSet):
    advertisement__title = CharFilter(lookup_expr='icontains',label='Заголовок')

    class Meta:
        model = Comment
        fields = ['advertisement__title', ]

