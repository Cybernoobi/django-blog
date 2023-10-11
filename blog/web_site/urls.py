from django.urls import path
from . import views

# http://127.0.0.1:8000/
# path(путь, что сделать, кроткое название)
# path(endpoint, view, name='url name')

urlpatterns = [
    path('', views.home_view, name='home'),
]