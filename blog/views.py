# from users.admin import CustomUserAdmin
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Document
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from users.models import CustomUser
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PublicPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description','text', 'allowed_list']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'allowed_list']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class DocumentView(generic.CreateView):
   
    model = Document
    fields = ('documents', 'name')
    template_name = 'blog/document_form.html'
 
    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
 
        # 紐づく記事を設定する
        document = form.save(commit=False)
        document.target = post
        document.name = self.request.user
        document.save()
 
        # 記事詳細にリダイレクト
        return redirect('blog:post-detail', pk=post_pk)
