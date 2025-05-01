from django.urls import path
from . import views

urlpatterns = [
    path('places/', views.list_tourist_places, name='list_tourist_places'),
    path('places/create/', views.create_tourist_place, name='create_tourist_place'),
    path('places/<int:pk>/', views.get_tourist_place_by_id, name='get_tourist_place_by_id'),
    path('places/<int:pk>/update/', views.update_tourist_place, name='update_tourist_place'),
    path('places/<int:pk>/delete/', views.delete_tourist_place, name='delete_tourist_place'),
]
