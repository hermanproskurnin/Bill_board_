from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Advertisement, Comment
from .forms import AdForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from .filters import CommentFilter
from django.contrib import messages

# отображает объявления
class AdvertisementList(ListView):
    model = Advertisement
    ordering = "-date_time"
    template_name = "advertisement.html"
    context_object_name = 'advertisements'

# страница конктретного объявления
class Ad(DetailView):
    model = Advertisement
    template_name = 'ad.html'
    context_object_name = 'ad'
    # отображает отклик
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.object
        context['comments'] = ad.comments.all()
        context['comment_form'] = CommentForm()
        return context

# создание объявления
class AdCreate(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdForm
    template_name = 'ad_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# редактирование
class AdUpdate(UpdateView):
    model = Advertisement
    form_class = AdForm
    template_name = 'ad_create.html'

    def get_queryset(self):
        # Фильтруем объявления по автору (текущему пользователю)
        return Advertisement.objects.filter(author=self.request.user)

# удаление
class AdDelete(DeleteView):
    model = Advertisement
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('advertisement_list')

    def get_queryset(self):
        # Фильтруем объявления по автору (текущему пользователю)
        return Advertisement.objects.filter(author=self.request.user)

# отклики
class CommentList(LoginRequiredMixin, ListView):
    model = Comment
    ordering = "-date_time"
    template_name = "comment_list.html"
    context_object_name = 'comments'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


@login_required()
def create_comment(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.advertisement = ad
            new_comment.save()

            messages.success(request, 'Ваш комментарий отправлен и ожидает одобрения.')
    return redirect('Ad', pk=pk)


@login_required
def like_ad(request, pk):
    ad = Advertisement.objects.get(pk=pk)
    ad.like += 1
    ad.save()
    return redirect('Ad', pk=pk)


@login_required
def dislike_ad(request, pk):
    ad = Advertisement.objects.get(pk=pk)
    ad.dislike += 1
    ad.save()
    return redirect('Ad', pk=pk)


@login_required
def approve_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.approve = True
    comment.save()
    return redirect('comment_list')


@login_required
def reject_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return redirect('comment_list')

