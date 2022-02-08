from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.all()
    #return HttpResponse("Estas en la pagina principal de Premios Platzi APP")
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })

def detail(request, question_id):
    #return HttpResponse(f"Estas viendo la pregunta numero {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {
        "question": question
    })

def results(request, question_id):
    #return HttpResponse(f"Estas viendo los resultados de la pregunta numero {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {
        "question": question
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) #choice hace referencia al atributo name del elemento RADIOINPUT
        print(selected_choice)
        #return HttpResponse(f"Estas votando a la pregunta numero {question_id}")

    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) #al trabajar con formularios se debe redirigir para no permitir al usuario enviar la resupuesta dos veces
        #el metodo reverse nos permite enviar el url pero en formato DJANGO para evitar hardcodear el url de igual forma que en el html