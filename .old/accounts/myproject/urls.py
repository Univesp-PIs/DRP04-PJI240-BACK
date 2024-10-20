from django.contrib import admin
from django.urls import path, include  # Incluindo 'include'
from login.views import home_view  # Importando a view home

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para o painel de admin do Django
    path('api/', include('login.urls')),  # Incluindo as URLs do aplicativo 'login'
    path('', home_view), # Rota para o caminho raiz
]
