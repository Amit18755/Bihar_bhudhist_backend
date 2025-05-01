from django.urls import path

from contactUs.views import ContactMessageByActionView, ContactMessageCreateView, ContactMessageListView, update_contact_action
 

urlpatterns = [
    path('contact/', ContactMessageCreateView.as_view(),name='create-message'),
    path('contact/messages/', ContactMessageListView.as_view(), name='show-message'),
    path('contact/messages/<str:action>/', ContactMessageByActionView.as_view(), name='contact-messages-by-action'),
    path('contact/messages/update/<int:pk>/', update_contact_action, name='update-contact-action'),
]
