from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
   list_display = ('id', 'firstname', 'lastname', 'email', 'phone')
   search_fields = ('firstname', 'lastname', 'email', 'phone')