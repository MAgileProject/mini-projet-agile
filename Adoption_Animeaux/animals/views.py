from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Animal
from .forms import AnimalForm

# 🔹 Liste animaux
class AnimalListView(ListView):
    model = Animal
    template_name = "animals/list.html"
    context_object_name = "animals"

# 🔹 Détails animal
class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animals/detail.html'


# Vérif rôle admin
class AdminRequired(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# 🔹 Ajouter animal (Admin)
class AnimalCreateView(LoginRequiredMixin, AdminRequired, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/form.html'
    success_url = reverse_lazy('animals:list')


# 🔹 Modifier animal (Admin)
class AnimalUpdateView(LoginRequiredMixin, AdminRequired, UpdateView):
    model = Animal
    form_class = AnimalForm
    
    
    template_name = 'animals/form.html'
    success_url = reverse_lazy('animals:list')


# 🔹 Supprimer animal (Admin)
class AnimalDeleteView(LoginRequiredMixin, AdminRequired, DeleteView):
    model = Animal
    template_name = 'animals/delete.html'
    success_url = reverse_lazy('animals:list')
