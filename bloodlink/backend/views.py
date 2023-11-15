from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(['POST'])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def user_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'User successfully logged out.'}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Add a check to ensure only the owner can update the user details
        if request.user != user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Add a check to ensure only the owner can delete the user
        if request.user != user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({'message': 'User successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
