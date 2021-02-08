from rest_framework import serializers

from todo.models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = serializers.ALL_FIELDS
        read_only_fields = ('created_by', 'status')

    created_by = serializers.StringRelatedField()
