from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework.routers import SimpleRouter
#from rest_framework.routers import DefaultRouter # get additional features compared to simple router
from rest_framework_nested import routers
from pprint import pprint
app_name = 'shop'
#router = SimpleRouter()
#router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
pprint(router.urls)

urlpatterns = router.urls + products_router.urls

# urlpatterns = [
#     #path('product/', views.ProductList.as_view()),
#     #path('product/<int:pk>/', views.ProductDetail.as_view()),
#     path('collection/', views.CollectionList.as_view(), name='collection-list'),
#     path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]

#urlpatterns = format_suffix_patterns(urlpatterns) # does not work in default router