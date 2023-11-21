from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Ici, vous pouvez ajouter les champs supplémentaires si nécessaire


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'



class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)
    
class Logout(LogoutView):
    template_name = 'task/logout.html'

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    

    def form_valid(self, form):
        form.save() # save the User
        return super().form_valid(form)

# Create your views here.

def CheckUserName(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        return HttpResponse('<div id="username-error" class="error" >Username already exists</div>', status=200)
    else:
        return HttpResponse('<div id="username-error" class="success" >Username is available</div>', status=200)     