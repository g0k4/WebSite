from django.shortcuts import render
from .models import News
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)

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


class NewCreateView(CreateView):
    model = News
    fields = [
        'title',
        'thumb',
        'content',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'thumb', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        new = self.get_object()
        if self.request.user == new.author:
            return True
        return False