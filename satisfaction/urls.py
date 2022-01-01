from django.urls import path
from satisfaction import views

urlpatterns = [
    path('create', views.satisfaction_all, name='create'),
    path('list', views.satisfaction_all, name='list'),
    path('read/<int:id>', views.satisfaction_by_id),
    path('update/<int:id>', views.satisfaction_by_id),
    path('delete/<int:id>', views.satisfaction_by_id),
]

