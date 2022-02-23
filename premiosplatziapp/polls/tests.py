from audioop import reverse
import datetime
from urllib import response

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

def create_question(question_text, days):
    """
    Create a question with the given question_text and published the given
    number of days offset to now (negative for past, positive for future)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no Questions exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index")) #hacer una peticion HTTP sobre el URL de index y guardar en response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], []) #verificar que el conjunto de preguntas esta vacio

    def test_question_published_in_future(self):
        """If a question whose pub_date is on th future, it should not be displayed"""
        #time = timezone.now() + datetime.timedelta(days=30)
        #future_question = Question(question_text="xxxxxxxxxxxxx",pub_date=time)
        #future_question.save()
        future_question = create_question("xxxxxx", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        self.assertNotContains(response, future_question)

    def test_question_published_in_past(self):
        """If a question whose pub_date is in the past, only that should be displayed"""
        #time = timezone.now() + datetime.timedelta(days=30)
        #future_question = Question(question_text="xxxxxxxxxxxxx",pub_date=time)
        #future_question.save()
        future_question = create_question("xxxxxx", -5)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [future_question])

    def test_future_questions_and_past_question(self):
        """
        Even if both past and future questions exists, only past questions are displayed
        """
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_questions(self):
        """The quesions index page may display multiple questions"""
        past_question1 = create_question(question_text="Past question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_questions(self):
        future_question1 = create_question(question_text="Future question 1", days=30)
        future_question2 = create_question(question_text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
    

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """If a user knows the url of a future question it should not be showed
        The detail view of a question with a pub_date in the future returns a 404 erro not found
        """
        future_question1 = create_question(question_text="Future question 1", days=30)
        url = reverse("polls:detail", args=(future_question1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question
        """
        past_question1 = create_question(question_text="Past question 1", days=-30)
        url = reverse("polls:detail", args=(past_question1.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question1.question_text)