from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('product/', views.product_list),
    path('product/<int:id>/', views.product_detail),
]