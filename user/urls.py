from django.urls import path
from .views import LoginView, UsersView, CargoCreateView, CargoListView, CarCreateView, RegisterView, VerifyView, \
    CargoDetailView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify', VerifyView.as_view()),
    path('login', LoginView.as_view()),
    path('list', UsersView.as_view()),
    path('detail/<int:pk>', UserDetailView.as_view()),
    path('cargo', CargoCreateView.as_view()),
    path('cargo/<int:pk>', CargoDetailView.as_view()),
    path('cargo/list', CargoListView.as_view()),
    path('car', CarCreateView.as_view()),

]
