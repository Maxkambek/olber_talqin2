from django.urls import path
from .views import LoginView, UsersView, CargoCreateView, CargoListView, RegisterView, VerifyView, \
    CargoDetailView, UserDetailView, CargoUDView, UserItemsView, LogoutView, DeleteAccountView, \
    OfferView, ChangePasswordView, ResetPasswordView, ConfirmResetPasswordView, CargoAcceptView, UserTypeView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify', VerifyView.as_view()),
    path('type', UserTypeView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('list', UsersView.as_view()),
    path('items/<int:pk>', UserItemsView.as_view()),
    path('changepassword', ChangePasswordView.as_view()),
    path('reset', ResetPasswordView.as_view()),
    path('confirm', ConfirmResetPasswordView.as_view()),


    path('detail/<int:pk>', UserDetailView.as_view()),
    path('cargo', CargoCreateView.as_view()),
    path('cargo/<int:pk>', CargoDetailView.as_view()),
    path('cargo/action/<int:pk>', CargoUDView.as_view()),
    path('cargo/list', CargoListView.as_view()),
    path('offer/<int:pk>', OfferView.as_view()),
    path('accept', CargoAcceptView.as_view()),

]
