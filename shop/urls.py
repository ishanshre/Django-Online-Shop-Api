from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'shop'
urlpatterns = [
    path('product/', views.ProductList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)