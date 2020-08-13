from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count


class Quiz(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название викторины')
    is_active = models.BooleanField(default=False, verbose_name='Викторина активна')
    user = models.ForeignKey(User, related_name='quizzes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_questions(self):
        return Question.objects.filter(quiz=self).order_by('id')

    def get_questions_count(self):
        return self.questions.all().count()

    def get_questions_cost(self):
        return self.questions.aggregate(Sum('cost'))


class Question(models.Model):
    text = models.TextField(verbose_name='Текст вопроса')
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    cost = models.IntegerField(verbose_name='Стоимость вопроса', default=0)

    def next_question(self, quiz=None):
        if quiz:
            return Question.objects.filter(quiz=quiz).order_by('id').first()
        else:
            return Question.objects.filter(id__gt=self.id, quiz=self.quiz).order_by('id').first()

    def __str__(self):
        return self.text


class Answer(models.Model):
    anstext = models.CharField(max_length=255, verbose_name='Вариант ответа')
    is_true = models.BooleanField(default=False, verbose_name='Правильный ответ')
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.anstext


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_true = models.BooleanField(default=False, verbose_name='Правильный ответ')
    cost = models.IntegerField(verbose_name='Стоимость вопроса', default=0)

    @staticmethod
    def get_cost_user_result(user, quiz_id):
        return UserAnswer.objects.filter(user=user, question__quiz_id=quiz_id).aggregate(Sum('cost'))

    @staticmethod
    def get_gamers(quiz_id):
        return UserAnswer.objects.filter(question__quiz_id=quiz_id).values('user__username').order_by('user__username').annotate(
            count=Count('user'), cost=Sum('cost'))

    @staticmethod
    def get_quizzes(user):
        return UserAnswer.objects.filter(user=user).values('question__quiz__name').order_by(
            'question__quiz__name').annotate(
            count=Count('question__quiz'), cost=Sum('cost'))