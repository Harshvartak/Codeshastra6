from .models import *
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=('head','description',)
