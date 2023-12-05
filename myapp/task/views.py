from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task
from django.views.decorators.http import require_POST

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Ici, vous pouvez ajouter les champs supplémentaires si nécessaire


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        # Si l'url ne contient pas de next
        if not self.request.GET.get("next"):
            return reverse_lazy("index")
        else:
            return super().get_success_url()

    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)


class Logout(LogoutView):
    template_name = "task/logout.html"


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()  # save the User
        return super().form_valid(form)


# Create your views here.


def CheckUserName(request):
    username = request.POST.get("username", None)
    data = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    if data["is_taken"]:
        return HttpResponse(
            '<div id="username-error" class="error" >Username already exists</div>',
            status=200,
        )
    else:
        return HttpResponse(
            '<div id="username-error" class="success" >Username is available</div>',
            status=200,
        )


class TasksView(LoginRequiredMixin, ListView):
    login_url = "/login"
    template_name = "task/tasks.html"
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()


@login_required
@require_POST
def add_task(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST.get("task_title", None)
        description = request.POST.get("task_description", None)
        user = request.user
        task = Task.objects.create(title=title, description=description)
        task.user.add(user)
        task.save()
        tasks = Task.objects.all()
        return render(request, "task/task_list.html", {"tasks": tasks})
    else:
        return render(request, "task/task_list.html", {})


@login_required
def delete_task(request, pk):
    if request.method == "DELETE":
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            task = Task.objects.all()
            return render(request, "task/task_list.html", {"tasks": task})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

    else:
        return render(request, "task/task_list.html", {})


def search_tasks(request):
    if request.method == "POST":
        search = request.POST.get("search", None)
        usertasks = request.user.tasks.all()
        results = Task.objects.filter(description__icontains=search).exclude(
            description__in=usertasks
        )

        return render(request, "task/search-result.html", {"tasks": results})
    else:
        return render(request, "task/search-result.html", {})
