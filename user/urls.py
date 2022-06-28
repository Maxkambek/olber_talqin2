from django.urls import path
from .views import *
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify', VerifyView.as_view()),
    path('type', UserTypeView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('items/<int:pk>', UserItemsView.as_view()),
    path('changepassword', ChangePasswordView.as_view()),
    path('reset', ResetPasswordView.as_view()),
    path('confirm', ConfirmResetPasswordView.as_view()),
    path('account', UserAccountView.as_view()),
    path('rating', AddPointView.as_view()),
    path('detail/<int:pk>', UserDetailView.as_view()),
    path('works', UserWorksView.as_view()),

    path('cargo', CargoCreateView.as_view()),
    path('cargo/<int:pk>', CargoDetailView.as_view()),
    path('cargo/action/<int:pk>', CargoUDView.as_view()),
    path('cargo/list', CargoListView.as_view()),
    path('offer/<int:pk>', OfferView.as_view()),
    path('accept', CargoAcceptView.as_view()),
    path('cargo/close/<int:pk>', CloseItemView.as_view()),

    path('work/list', WorkListView.as_view()),
    path('work/create', WorkView.as_view()),
    path('work/<int:pk>', WorkDetailView.as_view()),
    path('workes', UserWorkesView.as_view()),
    path('workoffer/<int:pk>', WorkOfferView.as_view()),
    path('workaccept', WorkAcceptView.as_view()),

]

