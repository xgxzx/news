from django.urls import path
from .views import *


urlpatterns = [
   path('', PostList.as_view()),
   path('index/', Index.as_view()),
   path('news/', PostList.as_view(), name='posts'),
   path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('news/search/', PostSearch.as_view(), name='posts_search'),
   path('news/create/', NewCreate.as_view(), name='create_news'),
   path('news/<int:pk>/edit/', NewEdit.as_view(), name='edit_news'),
   path('news/<int:pk>/delete/', NewDelete.as_view(), name='delete_news'),
   path('articles/create/', ArticlesCreate.as_view(), name='create_articles'),
   path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='edit_articles'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='delete_articles'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]
