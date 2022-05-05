from django.urls import path
from .views import LoginView, UsersView, CargoCreateView, CargoListView, CarCreateView, RegisterView, VerifyView

urlpatterns = [
    path('register/', LoginView.as_view()),
    path('verify', VerifyView.as_view()),
    path('login', LoginView.as_view()),
    path('users', UsersView.as_view()),
    path('cargo', CargoCreateView.as_view()),
    path('cargo/list', CargoListView.as_view()),
    path('car', CarCreateView.as_view()),

]
