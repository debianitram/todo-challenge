from django.contrib import admin
from django.utils.translation import gettext as _

from todo.models import ToDo


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_on', 'status')
    list_filter = ('status', )
    search_fields = ('content', )
    readonly_fields = ('status', )
    actions = ('action_mark_as_completed', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter_by_user(request.user)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def action_mark_as_completed(self, request, queryset):
        task_update_count = queryset.bulk_change_status(self.model.COMPLETED)
        self.message_user(request, f'Update {task_update_count} tasks!')

    action_mark_as_completed.short_description = _('Mark as completed!')
