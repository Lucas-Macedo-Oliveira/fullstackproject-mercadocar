from django.forms import ModelForm
from .models import Contato

class ContatoForm(ModelForm):
  class Meta:
    model = Contato
    fields = ['nome', 'email', 'mensagem']


from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['mensagem']