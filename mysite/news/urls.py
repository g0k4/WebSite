from django.urls import path
from . import views


app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='home'),
    path('<int:pk>', views.NewDetailView.as_view(), name='detail'),
    path('about', views.about_view, name='about'),
    path('create', views.NewCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.NewUpdateView.as_view(), name='update'),
    
    #path('create/',views.article_create, name="create"),
    #path('<int:number>/',views.arcticle_detail, name="detail"),
]
