"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import catalog.views

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', catalog.views.home, name='product_list'),

    path('cart/', catalog.views.cart_list, name='cart_list'),
    path('cart/<int:product_id>/add/', catalog.views.cart_add, name='cart_add'),
    path(
        'cart/<int:product_id>/delete/',
        catalog.views.cart_delete,
        name='cart_delete'
    ),

    path('admin/', admin.site.urls),
    url(r'api/', include('catalog.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
