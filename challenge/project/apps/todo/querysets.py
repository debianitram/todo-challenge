from django.db.models import QuerySet


class ToDoQuerySet(QuerySet):
    def filter_by_user(self, user):
        return self.filter(created_by=user)

    def bulk_change_status(self, status, *, tasks_id=None, user=None):
        queryset = self if tasks_id is None else self.filter(id__in=tasks_id)

        if user is not None:
            queryset = queryset.filter_by_user(user)

        return queryset.update(status=status)

    def filter_completed(self):
        return self.filter(status=self.model.COMPLETED)
