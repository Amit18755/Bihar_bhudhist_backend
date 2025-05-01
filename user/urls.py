from django.urls import path
from .views import CreateUserView, LoginView, ForgetPasswordView, SendOTPView, change_password, get_all_users, get_user_by_username, update_user_details, update_user_role

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('change-password/',change_password, name="change-password" ),
    path('details/', get_all_users, name='get_all_users'),
    path('update-role/', update_user_role, name='update_user_role'),
    path('get/<str:username>/', get_user_by_username),
    path('update/', update_user_details),
    path('otp/', SendOTPView.as_view(), name='sendOTP'),

]
