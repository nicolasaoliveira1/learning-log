from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
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

def new_entry(request, topic_id):
    """Adiciona uma nova anotação em um tópico específico"""
    topic = Topic.objects.get(id = topic_id)

    if request.method != "POST":
        #Nenhum dado foi enviado; cria form em branco
        form = EntryForm()
    else:
        #Dados POST encontrados; processamento dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse("topic", args=[topic_id]))
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)

def edit_entry(request, entry_id):
    """Edita um assunto existente de um tópico"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != "POST":
        #requisição inicial; preenche o formulário com informação atual
        form = EntryForm(instance=entry)

    else:
        #Dados de post submetidos; processa os dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("topic", args=[topic.id]))

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)