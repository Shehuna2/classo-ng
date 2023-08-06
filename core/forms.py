from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Topic, Exam, Contact

class TopicForm(forms.ModelForm):
    l_note = forms.CharField(widget=CKEditorWidget())
    l_plan = forms.CharField(widget=CKEditorWidget())
    tests = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Topic
        fields = ['subject', 'classroom', 'terms', 'weeks', 'name', 'l_note', 'l_plan', 'status']

class ExamForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Exam
        fields = ['subject', 'term', 'classroom', 'body', 'status']

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        
