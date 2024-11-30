from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('<int:R_ID>/select_time/', views.select_time, name='select_time'),
    path('<int:R_ID>/show_tables/<str:start_time>/', views.show_tables, name='show_tables'),
]
