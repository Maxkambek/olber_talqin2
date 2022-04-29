from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import LoginView, UsersView, CargoView

urlpatterns = [
    path('', include('rest_email_auth.urls')),
    path('login', LoginView.as_view()),
    path('users', UsersView.as_view()),
    path('cargo', CargoView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)