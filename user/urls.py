from django.urls import path, include
from .views import LoginView, UsersView

urlpatterns = [
    path('', include('rest_email_auth.urls')),
    path('login/', LoginView.as_view()),
    path('users', UsersView.as_view())
]