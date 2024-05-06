from django.urls import path
from .views import LoginView, RegisterView, GetUserView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('get-user/', GetUserView.as_view())
]