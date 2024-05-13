from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, ChangePasswordSerializer, GetUsersSerializer
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

        print(user)
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        serializer = self.serializer_class(user)

        uuid_str = str(user.id)
        
        payload = {
           'id': uuid_str,
           'exp': datetime.now(timezone.utc) + timedelta(minutes=1440)
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
        

class GetUserView(APIView):

    def get(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid Authorization header format')
        # token = request.COOKIES.get('jwt')

        token = authorization_header.split(' ',)[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


####################################################################
################################################
#########################################
########################
#change password




class ChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, id):
        password = request.data.get('password')
        new_password = request.data.get('new_password')

        obj = User.objects.get(pk=id)
        print(obj)
        if not obj.check_password(raw_password=password):
            return Response({'error': 'password do not match'}, status=400)
        else:
            obj.set_password(new_password)
            obj.save()
            return Response({'success': 'password changed successfully'}, status=200)


class GetUsers(APIView):
    serializer_class = GetUsersSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
