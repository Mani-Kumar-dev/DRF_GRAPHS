from rest_framework import generics
from .models import Data
from .serializers import DataSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, F
from datetime import datetime

class DataListView(generics.ListAPIView):
    serializer_class = DataSerializer

    def get_queryset(self):
        queryset = Data.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        category = self.request.query_params.get('category')

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        if category:
            queryset = queryset.filter(category=category)

        return queryset

@api_view(['GET'])
def chart_data(request):
    chart_type = request.query_params.get('type', 'line')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    category = request.query_params.get('category')

    queryset = Data.objects.all()
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])
    if category:
        queryset = queryset.filter(category=category)

    data = {
        'line': {
            'x': queryset.values_list('date', flat=True),
            'y': queryset.values_list('value', flat=True),
        },
        'bar': {
            'categories': queryset.values_list('category', flat=True).distinct(),
            'values': queryset.values('category').annotate(total=Sum('value')).values_list('total', flat=True),
        },
        'pie': {
            'labels': queryset.values_list('category', flat=True).distinct(),
            'sizes': queryset.values('category').annotate(total=Sum('value')).values_list('total', flat=True),
        }
    }

    return Response(data.get(chart_type, {}))
