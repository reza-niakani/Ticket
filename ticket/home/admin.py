from django.contrib import admin
from .models import Ticket,Answer

"""
    Introducing the built models to the Django admin 
    and displaying them in the Django admin panel 

"""

@admin.register(Ticket)

class TicketsAdmin(admin.ModelAdmin):
    list_display = ('user','title','created')
    search_fields = ('title','body')
    list_filter = ('created',)
    prepopulated_fields = {'title':('body',)}
    raw_id_fields = ('user',)

@admin.register(Answer)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user','ticket','is_answer')
    raw_id_fields = ('user','ticket','answer')
