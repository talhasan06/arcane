from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
class UserRegistrationFormView(FormView):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        user = form.save()
        user.is_active = False
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        confirm_link = f"http://127.0.0.1:8000/accounts/register/active/{uid}/{token}"
        login_link = "https://arcane-project.onrender.com/accounts/login/"
        email_subject = 'Verify Your Email'
        email_body=render_to_string('email_verification.html', {'confirm_link': confirm_link,'login_link':login_link})
        email = EmailMultiAlternatives(email_subject,'',to=[user.email])
        email.attach_alternative(email_body,"text/html")
        email.send()
        messages.success(self.request, 'Check your email for verification.')
        return super().form_valid(form)
    
def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = user._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginView(LoginView):
    template_name='user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(View):
     def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))
