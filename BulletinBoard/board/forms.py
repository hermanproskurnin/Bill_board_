from django import forms
from .models import Advertisement, Category, Comment


class AdForm(forms.ModelForm):
    advertisement_category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категории:'
    )

    class Meta:
        model = Advertisement
        fields = [
            'title',
            'content',
            'media_file',
            'advertisement_category',
        ]


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), label='Здесь отклик:')

    class Meta:
        model = Comment
        fields = ['content']
