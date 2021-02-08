import logging

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from todo.filters import ToDoFilter
from todo.models import ToDo
from todo.permissions import UserPermissions
from todo.serializers import ToDoSerializer


logger = logging.getLogger(__name__)


class ToDoViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (UserPermissions, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ToDoFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        logger.info(f"({instance.pk}) Delete tasks: {instance.content}")
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter_by_user(self.request.user)

    @action(
        methods=('post',),
        detail=False,
        url_path='mark_as_completed',
    )
    def mark_as_completed(self, request):
        if 'tasks_id' not in request.data:
            raise ValidationError('tasks_id values is required')

        tasks_id = request.data['tasks_id']
        update_tasks = self.queryset.bulk_change_status(
            ToDo.COMPLETED,
            tasks_id=tasks_id,
            user=request.user
        )
        data = {'count_tasks_completed': update_tasks}
        logger.info("Completed tasks with ids: %s", tasks_id)
        return Response(data=data, status=status.HTTP_200_OK)
