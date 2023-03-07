from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
]