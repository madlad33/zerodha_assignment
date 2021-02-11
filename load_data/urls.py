from django.urls import path, include
from .views import show_data,search_data
from django.views.generic import TemplateView
urlpatterns = [
# path('send/',TemplateView.as_view(template_name='show_data.html'),name='send'),
path('csv_data/',show_data,name='show'),
path('search/',search_data,name='search'),

]
