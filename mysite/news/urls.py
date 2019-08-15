from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='home'),
    path('<int:pk>', views.NewDetailView.as_view(), name='detail'),
    path('about', views.about_view, name='about'),
    path('create', login_required(views.NewCreateView.as_view()), name='create'),
    path('<int:pk>/update/', views.NewUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NewDeleteView.as_view(), name='delete'),

    
    #path('create/',views.article_create, name="create"),
    #path('<int:number>/',views.arcticle_detail, name="detail"),
]
