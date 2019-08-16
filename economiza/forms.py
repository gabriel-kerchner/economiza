# -*- coding: utf-8 -*-
from django import forms
from .models import Perfil, Gasto, Categoria
from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalForm


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome', 'sobrenome', 'sexo', 'idade', 'email', 'telefone']

class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

class GastoForm(BSModalForm):

    class Meta:
        model = Gasto
        fields = ['categoria', 'descricao', 'preco', 'quantidade']


class LimitGlobalForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ['limite']
        

class LimitCategoryForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['categoria_nome', 'limite_categoria']





        

