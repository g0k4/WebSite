from django.shortcuts import render,redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import News
from .models import Comment
from .forms import CreateComment
from profiles.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def about_view(request):
    return render(request,'news/about.html', {'title':'About'})

#detail new view
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


# News's class based views
# home page
class NewsListView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    ordering = ['-date_posted']


class NewDetailView(DetailView):
    model = News


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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        new = self.get_object()
        user = self.request.user
        # add admin fro delete
        if user == new.author:
            return True
        return False


class NewDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/news_delete.html'
    success_url = '/'

    def test_func(self):
        new = self.get_object()
        user = self.request.user
        # add admin fro delete
        if user == new.author:
            return True
        return False

 
# comment's class based views

class CommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
        update comment
    """
    model = Comment
    fields = ['content']
    template_name = 'comment/comment_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        # add admin fro delete
        if user == comment.author:
            return True
        return False


def delete_comment_view(request, pk, comment):
    comment = Comment.objects.get(id=comment)
    if request.user == comment.author:
        comment.delete()
        return redirect('news:detail', pk=pk)
    else:
        return redirect('news:home')


# delete comment
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