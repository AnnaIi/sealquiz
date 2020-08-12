from django.urls import path
from django.contrib.auth.decorators import login_required
from quiz.views import ActiveQuizView, QuizView, QuestionView, QuizEndView


urlpatterns = [

    path('quiz/<int:quiz_id>/quiz_end', login_required(QuizEndView.as_view()), name='quiz_end'),
    path('quiz/<int:quiz_id>/<int:question_id>', login_required(QuestionView.as_view()), name='question_url'),
    path('quiz/<int:quiz_id>', login_required(QuizView.as_view()), name='quiz_url'),
    path('', login_required(ActiveQuizView.as_view()), name='active_quizzes'),

]
