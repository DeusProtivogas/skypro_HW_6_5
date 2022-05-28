"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main import views, settings
from rest_framework import routers

from location.views import LocationViewSet

router = routers.SimpleRouter()
router.register("location", LocationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("api-auth/", include('rest_framework.urls')),
    path("categories/", views.CategoryListView.as_view()),
    path("categories/<int:category_id>", views.CategoryDetailView.as_view()),
    path("categories/create/", views.CategoryCreateView.as_view()),
    path("categories/<int:pk>/update/", views.CategoryUpdateView.as_view()),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view()),

    path("ads/", include("ads.urls")),
    path("users/", include("user.urls")),


    # View for loading data into database from json files
    path("add_info/", views.json_to_cat),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
