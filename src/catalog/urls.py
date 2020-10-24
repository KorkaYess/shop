from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from .views import ProductViewSet, CategoryViewSet, SubcategoryViewSet


router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products-viewset')
router.register('categories', CategoryViewSet, basename='category-viewset')
router.register(
    'subcategories', SubcategoryViewSet, basename='subcategory-viewset'
)
urlpatterns = [
    url(r'', include(router.urls))
]
