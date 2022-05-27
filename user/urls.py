from django.urls import path, re_path
from .views import LoginView, UsersView, CargoCreateView, CargoListView, CarCreateView, RegisterView, VerifyView, \
    CargoDetailView, UserDetailView, CargoUDView, UserItemsView, LogoutView, DeleteAccountView, TestCreateListView, \
    TestDetailView

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='OlBer API')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify', VerifyView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('list', UsersView.as_view()),
    path('items/<int:pk>', UserItemsView.as_view()),
    path('detail/<int:pk>', UserDetailView.as_view()),
    path('cargo', CargoCreateView.as_view()),
    path('cargo/<int:pk>', CargoDetailView.as_view()),
    path('cargo/action/<int:pk>', CargoUDView.as_view()),
    path('cargo/list', CargoListView.as_view()),
    path('car', CarCreateView.as_view()),
    path('testing', TestCreateListView.as_view()),
    path('testing/<int:pk>', TestDetailView.as_view()),
    re_path('docs', schema_view)
]
