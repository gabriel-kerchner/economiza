from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.contrib.auth.decorators import login_required
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView
from .models import Perfil, Gasto, Categoria
from .forms import PerfilForm, UserForm, GastoForm
from django.contrib import messages
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import json
import datetime



today = datetime.date.today()
# Create your views here.
def index(request):
    categorias = None
    value_limit_global = 0
    limit_by_category_id = {}
    has_at_least_one_category_limit = False
    if not request.user.is_anonymous:
        categorias = Categoria.objects.filter(user=request.user)
        value_limit_global = Perfil.objects.get(user=request.user).limite

        for categoria in categorias:
            limit_by_category_id[categoria.id] = categoria.limite_categoria
            if categoria.limite_categoria:
                has_at_least_one_category_limit = True

    return render(request,'economiza/index.html', {'categorias': categorias,
                                                   'value_limit_global': value_limit_global, 
                                                   'limit_by_category_id': limit_by_category_id})
                                                #    'has_at_least_one_category_limit': has_at_least_one_category_limit})

def about(request):
    return render(request, 'economiza/about.html')

def register_user(request):

    registered = False

    basic_categories = [u"Alimentação", u"Despesas do Lar", u"Lazer", u"Transporte", u"Outros"]

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if perfil_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit = False)
            perfil.user = user
            user.set_password(user.password)
            user.save()
            perfil.save()
            for category_name in basic_categories:
                category = Categoria(categoria_nome=category_name,
                                      user=user)
                category.save()
            

            registered = True
            login(request,user)

            return HttpResponseRedirect(reverse('economiza:index'))
        else:
            print(user_form.errors)
    else:

       user_form = UserForm() 
       perfil_form = PerfilForm()

    return render(request, 'economiza/cadastro.html', {'user_form': user_form, 'registered': registered, 'perfil_form': perfil_form})

def user_login(request):

    if request.method == 'POST':
     
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
        
            if user.is_active:
    
                login(request,user)
               
                return HttpResponseRedirect(reverse('economiza:index'))
            else:
    
                return HttpResponse("Your account is not active.")
        else:
            print("Erro ao login.")
            print("Campos: username: {} e password: {}".format(username,password))
            messages.error(request,'Usuário ou senha está incorreto!')
            return render(request, 'economiza/login.html')

    else:
        return render(request, 'economiza/login.html', {})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('economiza:index'))

@csrf_exempt
@login_required
def get_gastos(request):
     
    list_gastos = Gasto.objects.filter(user=request.user, data_do_gasto__month=today.month).order_by('data_do_gasto')        
    list_limits_categories = Categoria.objects.filter(user=request.user)
    gasto_form = GastoForm(request.POST)

    return render(request, 'economiza/gastos.html', {'gastos': list_gastos, 'gasto_form': gasto_form,
     'limites_categorias': list_limits_categories})


@csrf_exempt
@login_required
def select_month_year_and_category(request):
    
    if request.method == 'GET' and request.is_ajax():
        
        
        selected_month = request.GET['selected_month']
        selected_year = request.GET['selected_year']
        selected_category = request.GET['selected_category']
       
      
        if selected_month == '0' and selected_year == '0' and selected_category == '0':
            list_gastos = Gasto.objects.filter(user=request.user).order_by('data_do_gasto')
            

        if selected_month != '0' and selected_year == '0' and selected_category == '0': 
            list_gastos = Gasto.objects.filter(user=request.user, data_do_gasto__month=selected_month).order_by('data_do_gasto')
          

        if selected_year != '0' and selected_month == '0' and selected_category == '0':
            list_gastos = Gasto.objects.filter(user=request.user, data_do_gasto__year=selected_year).order_by('data_do_gasto')


        if selected_category != '0' and selected_month == '0' and selected_year == '0':
            list_gastos = Gasto.objects.filter(user=request.user, categoria__id=selected_category).order_by('data_do_gasto')

        if selected_category != '0' and selected_month != '0' and selected_year == '0':
            list_gastos = Gasto.objects.filter(user=request.user, data_do_gasto__month=selected_month,
                                                                  categoria__id=selected_category).order_by('data_do_gasto')

        if selected_category != '0' and selected_month == '0' and selected_year != '0':
            list_gastos = Gasto.objects.filter(user=request.user, data_do_gasto__year=selected_year,
                                                                  categoria__id=selected_category).order_by('data_do_gasto')

        if selected_year != "0" and selected_month != "0" and selected_category != "0":
            list_gastos = Gasto.objects.filter(user=request.user, data_do_gasto__month=selected_month,
                                                                  data_do_gasto__year=selected_year,
                                                                  categoria__id=selected_category).order_by('data_do_gasto')

        if selected_year != "0" and selected_month != "0" and selected_category == "0":
            list_gastos = Gasto.objects.filter(user=request.user, data_do_gasto__month=selected_month,
                                                                  data_do_gasto__year=selected_year).order_by('data_do_gasto')
    
    list_limits_categories = Categoria.objects.filter(user=request.user)
    gasto_form = GastoForm(request.POST)

    return render(request, 'economiza/filter_month_year_and_category.html', {'gastos': list_gastos, 'gasto_form': gasto_form,
     'limites_categorias': list_limits_categories})

@csrf_exempt
@login_required
def select_category(request):
    
    if request.method == 'GET' and request.is_ajax():
        selected_category = request.GET['selected_category']
        if selected_category == '0':
            list_limits_categories = Categoria.objects.filter(user=request.user)
        else:
            list_gastos = Gasto.objects.filter(user=request.user).order_by('data_do_gasto')
            list_limits_categories = Categoria.objects.filter(user=request.user, id__month=selected_month)
    else:
        selected_month = ''
        list_gastos = Gasto.objects.filter(user=request.user).order_by('data_do_gasto')

    
    
    gasto_form = GastoForm(request.POST)

    return render(request, 'economiza/filter_category.html', {'gastos': list_gastos, 'gasto_form': gasto_form,
     'limites_categorias': list_limits_categories})



class GastoCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'economiza/gasto_form.html'
    form_class = GastoForm
    success_url = reverse_lazy('economiza:get_gastos')


    def get_form(self, *args, **kwargs):
        form = super(GastoCreateView, self).get_form(*args, **kwargs)
        form.fields['categoria'].queryset = Categoria.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        return super().form_valid(form)

class GastoDeleteView(BSModalDeleteView):
    model = Gasto
    template_name = 'economiza/delete_gasto.html'
    success_url = reverse_lazy('economiza:get_gastos')
    success_message = ""



from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key) if dictionary.get(key) else ""


@login_required
def save_limits(request):

    if request.method=='POST' and request.is_ajax():
        value_global_limit = request.POST['value_global_limit']
        limit_by_category_id =  json.loads(request.POST['limit_by_category_id'])
        
        
        perfil = Perfil.objects.filter(user=request.user)
        perfil.update(limite=value_global_limit)

        categorias = Categoria.objects.filter(user=request.user)
        for categoria in categorias:
            categoria.limite_categoria = limit_by_category_id[str(categoria.pk)] or 0
            categoria.save()
        
        return HttpResponseRedirect(reverse('economiza:get_gastos'))
    
            
            
        