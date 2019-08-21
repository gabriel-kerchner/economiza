# -*- coding: utf-8 -*-
from django import forms
from .models import Perfil, Gasto, Categoria
from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalForm
from bootstrap_datepicker_plus import DatePickerInput
from tempus_dominus.widgets import DatePicker


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
    quantidade = forms.IntegerField(initial=1)
    data_do_gasto = forms.DateTimeField(widget=DatePicker(
        options={
            'format': 'D/MM/Y',
        },
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
        }
    ), input_formats=('%d/%m/%Y', ))
    class Meta:
        model = Gasto
        fields = ['data_do_gasto', 'categoria', 'descricao', 'preco', 'quantidade']
        ordering = ('data_do_gasto',)








        

