from django.contrib import admin
from django import forms
from .models import ChatRoom, User,ChatMessage
from django.core.exceptions import ValidationError
from django.db.models import Q


# Register your models here.
admin.site.register(User)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)

class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ChatRoomForm(forms.ModelForm):
     def clean(self):
         """
         This is the function that can be used to
         validate your model data from admin
         """
         super(ChatRoomForm, self).clean()
         first_person = self.cleaned_data.get('first_person')
         second_person = self.cleaned_data.get('second_person')

         lookup1 = Q(first_person=first_person) & Q(second_person=second_person)
         lookup2 = Q(first_person=second_person) & Q(second_person=first_person)
         lookup = Q(lookup1 | lookup2)
         qs = ChatRoom.objects.filter(lookup)
         if qs.exists():
             raise ValidationError(f'Thread between {first_person} and {second_person} already exists.')




