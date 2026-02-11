from django.views.generic import TemplateView


class SignupView(TemplateView):
    template_name = 'login.html'

class LoginView(TemplateView):
    template_name = 'signup.html'