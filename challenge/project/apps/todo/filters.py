from django_filters import rest_framework as rf_filters

from todo.models import ToDo


class ToDoFilter(rf_filters.FilterSet):
    class Meta:
        model = ToDo
        fields = ('content', 'created_on')

    content = rf_filters.CharFilter(field_name='content', lookup_expr='icontains')
    created_on = rf_filters.DateFilter(field_name='created_on', lookup_expr='date')
