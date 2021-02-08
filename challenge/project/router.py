from rest_framework.routers import DefaultRouter

from todo.views import ToDoViewSet

router = DefaultRouter()

router.register(prefix='todo', viewset=ToDoViewSet)
