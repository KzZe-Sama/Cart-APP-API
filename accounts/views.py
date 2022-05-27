from accounts.models import User
from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework import exceptions, serializers,status
from rest_framework.views import APIView,Response
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import GetAllUserSerializer, RegistrationSerializer,UserSerializer,CustomTokenObtainPairSerializer
# Create your views here.

USER = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer

class RegistrationView(APIView):
    permission_classes = (AllowAny,) 
    serializer_class = RegistrationSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"sucess":"Account has been created"}, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

class GetAllUserAPIView(ListAPIView):
    permission_classes = (IsAdminUser,IsAuthenticated)
    serializer_class = GetAllUserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)