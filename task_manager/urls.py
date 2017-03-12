from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from task_manager import views


router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]