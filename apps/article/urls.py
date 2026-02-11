from django.urls import path
from apps.article.views import(
     ArticleCreateView, ArticleDetailView, ArticleListView, CommetCreateView, ArticleDeleteView
)

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('detail/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('list/', ArticleListView.as_view(), name='article_list'),
    path('<slug:slug>/comment/', CommetCreateView.as_view(), name='comment_create'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
]