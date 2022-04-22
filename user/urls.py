from django.urls import path, include
from .views import LoginView

urlpatterns = [
    path('', include('rest_email_auth.urls')),
    path('login/', LoginView.as_view()),
]