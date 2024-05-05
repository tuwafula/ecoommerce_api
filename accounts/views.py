from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, status
from .models import User
import jwt
from datetime import datetime, timedelta, timezone


# Create your views here.


class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        serializer = self.serializer_class(user)

        uuid_str = str(user.id)
        
        payload = {
           'id': uuid_str,
           'exp': datetime.now(timezone.utc) + timedelta(minutes=60)
        }


        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()

        # response.set_cookie(key='jwt', value=token, httponly=True)

        # response.data = {'jwt' : token}

        if user.is_staff:
            response.data = {'jwt' : token, 'userType' : 'ADMIN'}
        else: 
            response.data = {'jwt' : token, 'userType' : 'REGULAR'}

        return response
        