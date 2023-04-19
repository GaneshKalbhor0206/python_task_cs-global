from django.urls import path
from .views import SignupAPIView, LoginAPIView, GetAllQuestionAPIView, vote

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('questions/', GetAllQuestionAPIView.as_view(), name='get_all_questions'),
    path('questions/<int:question_id>/vote/', vote, name='vote'),
]
