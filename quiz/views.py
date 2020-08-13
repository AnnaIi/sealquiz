from django.shortcuts import render
from django.views import View
from .models import Quiz, Question, Answer, UserAnswer
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect


class ActiveQuizView(View):

    def get(self, request):
        active_quizzes = Quiz.objects.filter(is_active=True)
        return render(request, 'quiz/active_quizzes.html', {'active_quizzes': active_quizzes})


class QuizView(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        first_question = Question().next_question(quiz=quiz)
        return render(request, 'quiz/quiz.html', {'quiz': quiz, 'first_question': first_question})


class QuestionView(View):

    def get(self, request, quiz_id, question_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        question = get_object_or_404(Question, pk=question_id, quiz_id=quiz)
        next_question = question.next_question()
        gamers = UserAnswer.get_gamers(quiz.id)
        return render(request, 'quiz/question.html',
                      {'quiz': quiz, 'question': question, 'next_question': next_question, 'gamers':gamers})

    def post(self, request, quiz_id, question_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        question = get_object_or_404(Question, pk=question_id, quiz_id=quiz)
        answer_id = request.POST.get('answer')
        answer = get_object_or_404(Answer, pk=answer_id, question=question)
        result, created = UserAnswer.objects.get_or_create(user=request.user,
                                                           question=question,
                                                           defaults={'answer': answer,'is_true': answer.is_true,
                                                                                    'cost': question.cost if answer.is_true else 0})
        next_question = question.next_question()

        if next_question:
            return redirect('question_url', quiz.id, next_question.id)
        else:
            return redirect('quiz_end', quiz.id)


class QuizEndView(View):

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        cost = UserAnswer.get_cost_user_result(request.user, quiz.id)
        return render(request, 'quiz/end.html',
                      {'quiz': quiz, 'cost': cost})


class MyStatView(View):
    def get(self, request):
        quizzes = UserAnswer.get_quizzes(request.user)
        return render(request, 'quiz/statistic.html',
                      {'quizzes':quizzes})

