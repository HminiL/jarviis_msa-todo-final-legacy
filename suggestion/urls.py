from django.urls import path, re_path
from suggestion import views

urlpatterns = [
    path('create', views.suggestion_all, name='create'),
    path('list', views.suggestion_all, name='list'),
    path('read/<int:id>', views.suggestion_by_id),
    path('update/<int:id>', views.suggestion_by_id),
    path('delete/<int:id>', views.suggestion_by_id),
    path('user/<int:user_id>', views.suggestion_user),
    path('user/test/<int:user_id>', views.suggestion_user_test),
    path('accept', views.suggestion_accept),
    path('reject', views.suggestion_reject),
    path('test', views.test),
    # path('', views.index),
]