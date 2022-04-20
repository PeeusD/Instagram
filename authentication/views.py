from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

User = get_user_model()
class SignUpView(View):
    form_class = UserForm
    def get(self, request, *args, **kwargs):

        return render(request, 'authentication/signup.html')
        
    def post(self, request, *args, **kwargs):
        #user signup
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
            
        return render(request, 'authentication/signup.html', {'form': form})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    # success_message = "We've emailed you instructions for setting your password, " \
    #                   "if an account exists with the email you entered. You should receive them shortly." \
    #                   " If you don't receive an email, " \
    #                   "please make sure you've entered the address you registered with, and check your spam folder."
    
class LogInView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_feed')
        return render(request, 'authentication/login.html')
        
    def post(self, request, *args, **kwargs):
       
        #user login using username or email
        email_username = request.POST.get('email_username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=email_username)
            email = user_obj.email
        except Exception as e:
            email = email_username
            print(e)
      
        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials :(')
            return render(request, 'authentication/login.html')
        login(request, user)
        # messages.success(request, "Thankyou ! welcome to insta-clone")
        return redirect ('home_feed')

class LogOutView(View):
    def post(self, request,  *args, **kwargs): 
        logout(request)
        return redirect('log_in')
      



    