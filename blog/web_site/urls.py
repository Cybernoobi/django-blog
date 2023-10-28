from django.urls import path
from . import views

# http://127.0.0.1:8000/
# path(путь, что сделать, кроткое название)
# path(endpoint, view, name='url name')

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/<str:category_id>/', views.category_articles, name="category_articles"),
    path('articles/<str:article_id>/', views.article_detail, name='article_detail'),

    path('login/', views.login_view, name="login"),
    path('registration/', views.registration_view, name="registration"),
    path('logout/', views.user_logout, name="logout"),

    path('create/article/', views.created_article, name="create")
]