from rest_framework.viewsets import ModelViewSet
from .serializer import ProjectSerializer, TaskSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Task,Project
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.core.cache import cache
from rest_framework.response import Response
from django_redis import get_redis_connection
from .tasks import send_deadline_reminder


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def invalidate_user_project_cache(self,user_id):
        conn = get_redis_connection('default')
        pattern= f"projects:{user_id}:*"
        keys = list(conn.scan_iter(pattern))
        if keys: 
            conn.delete(*keys)
    

    def list(self, request, *args, **kwargs):
        cache_key = f"projects:{request.user.id}:{request.query_params.urlencode()}"
        cached =cache.get(cache_key)
        if cached:
            return Response(cached)
        
        response =  super().list(request, *args, **kwargs)
        cache.set(cache_key,response.data,timeout=60)
        return response

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.save(owner=user)
        self.invalidate_user_project_cache(user.id)
        return data

    def perform_destroy(self, instance):
        user = self.request.user
        instance.delete()
        self.invalidate_user_project_cache(user.id)

    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.save()
        self.invalidate_user_project_cache(user.id)
        return data
    
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'priority', 'project']
    ordering_fields = ['created_at', 'updated_at', 'priority', 'due_date']
    search_fields = ['title', 'description']

    def invalidate_user_task_cache(self, user_id):
        conn = get_redis_connection("default")
        pattern = f"tasks:{user_id}:*"
        keys = list(conn.scan_iter(pattern))
        if keys: 
            conn.delete(*keys)
    

    def list(self, request, *args, **kwargs):
        cache_key = f"tasks:{request.user.id}:{request.query_params.urlencode()}"
        cached = cache.get(cache_key)
        if cached:
            print(cached)
            return Response(cached)
        
        response =  super().list(request, *args, **kwargs)
        cache.set(cache_key,response.data,timeout=60)
        return response

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        task =  serializer.save(owner=user)
        send_deadline_reminder.delay(task.id)
        self.invalidate_user_task_cache(user.id)
        return task
    
    def perform_destroy(self, instance):
        user = self.request.user
        instance.delete()
        self.invalidate_user_task_cache(user.id)

    def perform_update(self, serializer):
        user = self.request.user
        task = serializer.save()
        self.invalidate_user_task_cache(user.id)
        return task
    