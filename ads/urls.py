
from django.urls import path


from ads import views

urlpatterns = [
    path("", views.AdListView.as_view()),
    path("<int:pk>/", views.AdDetailView.as_view()),
    path("create/", views.AdCreateView.as_view()),
    path("<int:pk>/update/", views.AdUpdateView.as_view()),
    path("<int:pk>/delete/", views.AdDeleteView.as_view()),
    path("<int:pk>/image/", views.AdImageView.as_view()),
    path('selection/', views.SelectionListView.as_view()),
    path('selection/<int:pk>/', views.SelectionRetrieveView.as_view()),
    path('selection/create/', views.SelectionCreateView.as_view()),
    path('selection/<int:pk>/update/', views.SelectionUpdateView.as_view()),
    path('selection/<int:pk>/delete/', views.SelectionDeleteView.as_view()),
]