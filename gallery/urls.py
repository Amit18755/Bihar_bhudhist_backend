from django.urls import path
from .views import PlaceCreateView, PlaceDeleteView,  PlaceListView, delete_place_image, get_images_by_place, upload_place_image

urlpatterns = [
    path('places/create/', PlaceCreateView.as_view(), name='place-create'),
    path('places/list/', PlaceListView.as_view(), name='place-list'),
    path('places/delete/<int:id>/', PlaceDeleteView.as_view(), name='place-delete'),
    path('places/image/upload/', upload_place_image, name='place_image_upload'),
    path('places/<int:place_id>/images/', get_images_by_place, name='get_images_by_place'),
    path('places/image/delete/<int:image_id>/', delete_place_image, name='delete_place_image'),
]
