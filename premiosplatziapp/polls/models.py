from datetime import datetime
from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
#aqui va todo lo relacionado a DATOS

class Question(models.Model):
    #id # no hace falta tener este atributo, DJANGO lo crea y lo aumenta automaticamente
    question_text = models.CharField(max_length=200) #equivale al VARCHAR en la BD
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #cascade sirve para eliminar todas las opciones de esta QUESTION
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text