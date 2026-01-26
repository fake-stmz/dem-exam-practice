from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def index(request):

    if not request.session.get("redirected_to_login", False):
        request.session["redirected_to_login"] = True
        return redirect("login")

    current_user = request.user

    if current_user.groups.filter(name="Авторизированный клиент").exists():
        return render(request, "index_client.html")

    if current_user.groups.filter(name="Менеджер").exists():
        return render(request, "index_manager.html")

    if current_user.groups.filter(name="Администратор").exists():
        return render(request, "index_admin.html")


    return render(request, "index.html")


def login_view(request):

    if request.method == "POST":
        login_input = request.POST.get("login")
        password = request.POST.get("password")

        user = authenticate(request, username=login_input, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"error": "Неверный логин или пароль."})

    return render(request, "login.html")


def logout_view(request):

    logout(request)
    request.session["redirected_to_login"] = True

    return redirect("login")