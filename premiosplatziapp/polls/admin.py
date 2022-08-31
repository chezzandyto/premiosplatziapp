from dataclasses import fields
from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

#personaliza como se ve el modelo Question en el administrador de django
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [ChoiceInline] #esta linea sirve para en el admin de django ubicar tambien las choices y crearlas de una vez




admin.site.register(Question, QuestionAdmin) #esto hace que el modelo sea registrado en el administrador de datos

