from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('tasks', views.TasksView.as_view(), name='tasks'),
    path('task/create', views.add_task, name='task_create'),
    path('task/<int:pk>/delete', views.delete_task, name='task_delete'),

]

htmx_views = [
    path('check_username', views.CheckUserName, name='check_username'),
    path("search", views.search_tasks, name="search_task"),
]
urlpatterns += htmx_views