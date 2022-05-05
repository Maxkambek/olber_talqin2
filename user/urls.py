from django.urls import path, include
from .views import LoginView, UsersView, CargoCreateView, CargoListView

urlpatterns = [
    path('', include('rest_email_auth.urls')),
    path('login', LoginView.as_view()),
    path('users', UsersView.as_view()),
    path('cargo', CargoCreateView.as_view()),
    path('cargo/list', CargoListView.as_view())

]
