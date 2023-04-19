from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, QuestionSerializer, ChoiceSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Choice, Question
from rest_framework.pagination import CursorPagination

# Define the cursor-based pagination class for Questions
class QuestionCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'  # Replace 'id' with the field you want to order by

# SignupAPIView allows a user to sign up for an account
class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user_id': user.id,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# LoginAPIView allows a user to log in to their account
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# GetAllQuestionAPIView returns all Questions with cursor-based pagination
class GetAllQuestionAPIView(APIView):
    pagination_class = QuestionCursorPagination

    def get(self, request):
        questions = Question.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(questions, request)
        serializer = QuestionSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

# Vote API allows authenticated users to vote on a specific Choice
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vote(request, question_id):
    choice_text = request.data.get('Choice_text')
    if not choice_text:
        return Response({'Status_code': 400, 'Result': 'Choice_text is required.'}, status=400)
    choice = get_object_or_404(Choice, question_id=question_id, choice_text=choice_text)
    choice.votes += 1
    choice.save()
    serializer = ChoiceSerializer(choice)
    return Response({'Status_code': 200, 'Result': 'SUCCESS', 'data': serializer.data}, status=200)
