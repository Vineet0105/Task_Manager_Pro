from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from accounts.views import RegisterAPIViews
from tasks.views import TaskViewSet, ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tasks',TaskViewSet,basename='task')
router.register('projects',ProjectViewSet,basename='project')



urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_view'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('register/',RegisterAPIViews.as_view(),name='register_user'),
    path('',include(router.urls)),
]