from django.urls import path
from . import views 

urlpatterns = [
    path('basics/area-triangulo',  views.area_triangulo),
    path('basics/tabla-multiplicar', views.tabla_multiplicar),
    path('basics/contar-mayores', views.contar_mayores),
    path('basics/suma-descendente', views.suma_descendente),
    path('basics/promedio-lista', views.promedio_lista),
]