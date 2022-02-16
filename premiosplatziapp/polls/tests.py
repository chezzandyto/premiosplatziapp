from audioop import reverse
import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls.base import reverse

class QuestionModelTests(TestCase): #heredar de testcase nos permiten traer una bateria de tests

    def test_was_published_recently_with_future_questions(self):
        """Was_published_recently returns FALSE for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quien es el mejor Course Director de Platzi",pub_date=time)
        self.assertIs(future_question.was_published_recently(),False) # verifica con el metodo assert si el resultado de la funcion es igual a false

    def test_was_pulished_recently_with_today_questions(self):
        """was_published_recently should return True for questions whose pub_date is today"""
        time = timezone.now()
        question = Question(question_text="Quien es el mejor Course Director de Platzi",pub_date=time)
        self.assertEquals(question.was_published_recently(),True)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently should return flase for questions whose pub_date was yesterday or more"""
        time = timezone.now() - datetime.timedelta(days=10)
        past_question = Question(question_text="Quien es el mejor Course Director de Platzi",pub_date=time)
        self.assertEquals(past_question.was_published_recently(),False)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no Questions exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index")) #hacer una peticion HTTP sobre el URL de index y guardar en response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], []) #verificar que el conjunto de preguntas esta vacio