from django.urls import path
from .views import (
    OverviewListView,
    OverviewCreateView,
    OverviewUpdateView,
)
from .views import (
    OverviewImageListView,
    OverviewImageCreateView,
    OverviewImageUpdateView,
    OverviewImageDeleteView,
)
urlpatterns = [
    path('list/', OverviewListView.as_view(), name='overview-list'),
    path('create/', OverviewCreateView.as_view(), name='overview-create'),
    path('update/<int:pk>/', OverviewUpdateView.as_view(), name='overview-update'),


    path('images/list/', OverviewImageListView.as_view(), name='overviewimage-list'),
    path('images/create/', OverviewImageCreateView.as_view(), name='overviewimage-create'),
    path('images/update/<int:pk>/', OverviewImageUpdateView.as_view(), name='overviewimage-update'),
    path('images/delete/<int:pk>/', OverviewImageDeleteView.as_view(), name='overviewimage-delete'),
]
