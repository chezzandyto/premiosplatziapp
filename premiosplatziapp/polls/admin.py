from django.contrib import admin
from .models import Question

admin.site.register(Question) #esto hace que el modelo sea registrado en el administrador de datos

