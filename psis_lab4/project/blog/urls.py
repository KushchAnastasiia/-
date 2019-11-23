from django.urls import path

from .views import ArticlesList, ArticleCreate


urlpatterns = [
    path('', ArticlesList.as_view(), name='main'),
    path('create/', ArticleCreate.as_view(), name='create')
]
