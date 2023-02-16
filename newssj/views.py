from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponse
from .filters import PostFilter
from .models import Post, Category, Subscriber
from .forms import PostForm
from .tasks import *


class PostList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'news/search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsSJ.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.publication_type = 'NW'
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsSJ.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.publication_type = 'AR'
        return super().form_valid(form)


class NewEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsSJ.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class ArticlesEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsSJ.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class NewDelete(DeleteView):
    raise_exception = True
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('posts')


class ArticlesDelete(DeleteView):
    raise_exception = True
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('posts')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'news/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class Index(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hi!')
