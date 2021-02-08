from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from todo.querysets import ToDoQuerySet


class ToDo(models.Model):
    class Meta:
        verbose_name = _('To Do')
        verbose_name_plural = verbose_name

    NEW = 'new'
    COMPLETED = 'completed'

    STATUS = (
        (NEW, _('New')),
        (COMPLETED, _('Completed')),
    )

    content = models.CharField(max_length=50)
    status = models.CharField(max_length=9, choices=STATUS, default=NEW)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    objects = ToDoQuerySet.as_manager()

    def __str__(self):
        return f'#To Do: {self.content}'

    def mark_as_completed(self):
        self.status = self.COMPLETED
        self.save(update_fields=('status', ))
