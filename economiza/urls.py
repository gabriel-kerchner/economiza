from django.urls import path, include
from economiza import views


app_name = 'economiza'


urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('extrato/', views.get_gastos, name='get_gastos'),
    path('gastos/adicionar', views.GastoCreateView.as_view(), name='add_gasto'),
    path('gastos/apagar/<int:pk>', views.GastoDeleteView.as_view(), name='delete_gasto'),
    path('salvar-limite/', views.save_limits, name='save_limits'),
    path('select_month_year_and_category/', views.select_month_year_and_category, name='selected_month'),
    path('sobre/', views.about, name='about')
]
