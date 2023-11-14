from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    template_name = 'login.html'

class Logout(LogoutView):
    template_name = 'task/logout.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    

    def form_valid(self, form):
        form.save() # save the User
        return super().form_valid(form)

# Create your views here.
