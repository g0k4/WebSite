from django.urls import path
from . import views


app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='home'),
    # path('<int:pk>', views.NewDetailView.as_view(), name='detail'),
    path('<int:pk>', views.detail_view, name='detail'),
    
    path('ping', views.ping_view, name='ping'),
    path('create', views.NewCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.NewUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NewDeleteView.as_view(), name='delete'),
    
    # comments links
    path('comment/update/<int:pk>', views.CommentUpdateView.as_view(), name='comment_update'),
    path('<int:pk>/delete_comment/<int:comment>', views.delete_comment_view, name='comment_delete'),
    # path('comment/delete/<int:pk>', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('search/', views.search_view, name="search"),
]
