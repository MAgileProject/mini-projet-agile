from django.shortcuts import render

# Create your views here.
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['action'] = "Modifier" if self.object else "Ajouter"
    return context
