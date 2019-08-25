from django.shortcuts import render,redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import News, Comment
from .forms import CreateComment
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from profiles.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def ping_view(request):
    if request.user.is_superuser:
        import subprocess
        if request.method == 'POST':
            host = request.POST['host']
            command = ['ping', '-c','1',host]
            # with output in infor
            # info = subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
            code = subprocess.run(command, stdout=subprocess.PIPE).returncode
            if not code:
                messages.success(request, host+f' is up')
            else:
                messages.error(request, host+f' is down')

    return redirect('news:home')


def home_view(requset):
    news = News.objects.all().filter(date_posted)
    return render(request, 'news/home.html', {
        'news':news,
    })


def detail_view(request, pk):
    new = News.objects.get(id=pk)
    comments = Comment.objects.filter(new=new)[::-1]

    if request.method == 'POST' :
        form = CreateComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.new = new
            comment.author = request.user
            comment.save()
            return redirect('news:detail', pk=pk)
    else:
        form = CreateComment()

    return render(request, 'news/news_detail.html', {
        'new':new,
        'form':form,
        'comments':comments
    })


def search_view(request):
    search_query = request.GET.get('search','')
    news = None
    users = None

    if search_query:
        news = News.objects.filter(Q(title__icontains=search_query)| Q(content__icontains=search_query))
        users = User.objects.filter(username__icontains=search_query)
    
    return render(request, 'news/search.html',{
        'news':news,
        'users':users,
    })



class NewsListView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    ordering = ['-date_posted']


class NewCreateView(LoginRequiredMixin, CreateView):
    model = News
    fields = [
        'title',
        'thumb',
        'content',
    ]
    template_name = 'news/news_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'thumb', 'content']
    template_name = 'news/news_update.html'

    def test_func(self):
        new = self.get_object()
        user = self.request.user
        if user == new.author or user.is_superuser:
            return True
        return False


class NewDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/news_delete.html'
    success_url = '/'

    def test_func(self):
        new = self.get_object()
        user = self.request.user
        if user == new.author or user.is_superuser:
            return True
        return False


class CommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'comment/comment_update.html'

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        if user == comment.author or user.is_superuser:
            return True
        return False


def delete_comment_view(request, pk, comment):
    comment = Comment.objects.get(id=comment)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
        return redirect('news:detail', pk=pk)
    else:
        return redirect('news:home')


"""
class NewDetailView(DetailView):
    model = News
"""


"""
class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        # add admin fro delete
        if user == comment.author:
            return True
        return False

"""