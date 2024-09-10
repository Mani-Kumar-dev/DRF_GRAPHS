from django.urls import path
from .views import DataListView, chart_data

urlpatterns = [
    path('data/', DataListView.as_view(), name='data-list'),
    path('chart/', chart_data, name='chart-data'),
]
