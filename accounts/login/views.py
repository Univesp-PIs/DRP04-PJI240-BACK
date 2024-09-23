import time
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse


SECRET_KEY = 'sua_chave_secreta'
def home_view(request):
    return HttpResponse("Bem-vindo à API! Acesse http://127.0.0.1:8000/api/admin/login para o login.")

class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username == 'admin' and password == '1234':
            expiry_timestamp = int(time.time()) + 1800
            token = jwt.encode({'user_id': 1, 'exp': expiry_timestamp}, SECRET_KEY, algorithm='HS256')

            return Response({
                "message": "Login realizado com sucesso",
                "payload": {
                    "token": token,
                    "expiry_timestamp": expiry_timestamp,
                    "user_id": 1
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuário ou senha inválido"}, status=status.HTTP_403_FORBIDDEN)
