import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question

class QuestionModelTests(TestCase): #heredar de testcase nos permiten traer una bateria de tests

    def test_was_published_recently_with_future_questions(self):
        """Was_published_recently returns FALSE for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quien es el mejor Course Director de Platzi",pub_date=time)
        self.assertIs(future_question.was_published_recently,False) # verifica con el metodo assert si el resultado de la funcion es igual a false
        