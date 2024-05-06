from django.urls import path
from .views import LoginView, RegisterView, GetUserView, ChangePassword


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('get-user/', GetUserView.as_view()),
    path('change_password/<str:id>/', ChangePassword.as_view(), name='change_password'), 
]