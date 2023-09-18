from django.urls import path

from data_app.views import index

urlpatterns = [
    path('', index, name='test')
]
