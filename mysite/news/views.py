from django.shortcuts import render,redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import News
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# from .forms import CreateNew

# Create your views here.

def about_view(request):
    return render(request,'news/about.html', {'title':'About'})


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
"""
def create_view(request):
    if request.method == 'POST':
        form = CreateNew(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            return redirect('news:home')
    else:
        form = CreateNew()
    return render(request, 'news/news_form.html', {
        'form':form 
    })
"""