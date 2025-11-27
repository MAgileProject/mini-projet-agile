from django.views.generic import ListView, DetailView
from .models import Animal

class AnimalListView(ListView):
    model = Animal
    template_name = 'animals/list.html'
    context_object_name = 'animals'
    paginate_by = 12

class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animals/detail.html'
