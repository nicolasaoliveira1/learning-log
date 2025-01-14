from django.shortcuts import render
from .models import Topic
from .forms import TopicForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    """Página principal do Learning_Log."""
    return render(request, "learning_logs/index.html")

def topics(request):
    """Mostra todos os assuntos."""
    topics = Topic.objects.order_by('date_added')
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)

def topic(request,topic_id):
    """Mostra todos as entradas de um tópico"""
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)

def new_topic(request):
    """Adiciona um novo tópico."""
    if request.method != "POST":
        #Nenhum dado submetido; cria um formulário em branco
        form = TopicForm()
    else:
        #Dados de POST submetidos; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("topics"))
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)