from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import template
    
register = template.Library()


# Create your models here.
class Categoria(models.Model):

    categoria_nome = models.CharField(max_length=128)
    limite_categoria = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='categoria', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.categoria_nome


class Perfil(models.Model):
    SEXO_CHOICES = [
        ["F", "Feminino"],
        ["M", "Masculino"],
        ["N", "Nenhuma das opções"]
    ]

    nome = models.CharField(max_length=128, null=False)
    sobrenome = models.CharField(max_length=128, null=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    idade = models.IntegerField(null=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(null=False, unique=True)
    user = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    limite = models.PositiveIntegerField(null=True)
    criado_em = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ['criado_em']
        verbose_name = (u'Perfil')
        verbose_name_plural = (u'Perfis')

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('economiza:get_gastos', kwargs={'pk': self.pk})


class Gasto(models.Model):
  
    data_do_gasto = models.DateField(null=True)
    categoria = models.ForeignKey(Categoria, related_name='gasto', on_delete=models.CASCADE)
    descricao = models.CharField(max_length=150)
    preco = models.FloatField()
    quantidade = models.PositiveIntegerField()
    user = models.ForeignKey(User, related_name='gasto', on_delete=models.CASCADE, null=True)

    @register.filter
    def total_item_filter(self):
        return  self.quantidade * self.preco

    @property
    def limite_modify(self):
        return self.limite - self.total_item_filter





    

