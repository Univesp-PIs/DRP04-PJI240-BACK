from django.urls import path
from login.views import AdminLoginView  # Caso o nome da nova pasta seja 'login'


urlpatterns = [
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
]
