import secrets
import string
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response

from django.core.mail import send_mail
from django.conf import settings


# Read all users
@api_view(['GET'])
def getAllUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# user login point
@api_view(['GET'])
def login(request, pk=None):
    try:
        instance = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(instance)
    return Response(serializer.data)


# user registratin point
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user reset password point
@api_view(['PUT'])
def updateSingleUser(request, user_id):
    password = request.data.get('password')
    email = request.data.get('email')
    user = User.objects.filter(id=user_id).first()

    if user is None:
        response_data = { "response": "password not set" }
        return Response(response_data, status = status.HTTP_404_NOT_FOUND)

    user.password = password
    user.email = email
    user.save()
    response_data = { "response": "user password updated" }
    return Response(response_data, status = status.HTTP_200_OK)


# delete a user from the table
@api_view(['DELETE'])
def deleteSingleUser(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        response_data = { "response": "User deleted" }
        return Response(response_data, status = status.HTTP_200_OK)
    except User.DoesNotExist:
        return HttpResponse('User not found', status=404)


# reset user password
class passwordReset:
    def __init__(self):
        pass

    def generate_random_link(self, length=24):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def send_reset_password_email(self, user, reset_link):
        subject = 'Password Reset Link'
        message = f'Click the following link to reset your password: {reset_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

    def get_user_by_email(self, email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None

    def reset_password_for_user(self, email):
        user = self.get_user_by_email(email)
        if user:
            reset_link = self.generate_random_link()
            self.send_reset_password_email(user, reset_link)
            return HttpResponse("Link to reset sent.")
        else:
            return "User not found."

# Usage
# if __name__ == '__main__':
#     prh = passwordReset()
#     email = "user@example.com"
#     result = prh.reset_password_for_user(email)
#     print(result)
