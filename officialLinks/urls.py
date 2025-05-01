from django.urls import path
from .views import create_official_link, delete_official_link, get_official_link_by_id, list_official_links, update_official_link

urlpatterns = [
    path('create/', create_official_link, name='create_official_link'),
    path('list/', list_official_links, name='list_official_links'),
    path('delete/<int:pk>/', delete_official_link, name='delete_official_link'),
    path('update/<int:pk>/', update_official_link, name='update_official_link'),
    path('get/<int:pk>/', get_official_link_by_id, name='get_official_link_by_id'),
]
