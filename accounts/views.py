from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
class CreateUserView(View):
    def get(self, request):
        return render(request, "accounts/create_user.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != "" and password == password2:
            u = User(username=username)
            u.set_password(password)
            u.save()
            return redirect('home')
        return render(request, "accounts/create_user.html", {"error": "Hasła nie są zgodne"})


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            redirect_url = request.GET.get('next', 'home')
            login(request, user)
            return redirect(redirect_url)
        else:
            error = "Nieprawidłowa nazwa użytkownika lub hasło"
            return render(request, "accounts/login.html", {'error': error})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
