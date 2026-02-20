from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Product


def index(request):

    if not request.session.get("redirected_to_login", False):
        request.session["redirected_to_login"] = True
        return redirect("login")

    products = (Product.objects.all()
                .select_related("category")
                .select_related("supplier")
                .select_related("producer")
                .select_related("measure_unit"))

    context = {
        "products": products
    }

    current_user = request.user

    if current_user.groups.filter(name="Авторизированный клиент").exists():
        return render(request, "index_client.html", context)

    if current_user.groups.filter(name="Менеджер").exists():
        return render(request, "index_manager.html", context)

    if current_user.groups.filter(name="Администратор").exists():
        return render(request, "index_admin.html", context)

    return render(request, "index.html", context)


def search_view(request):

    query = request.GET.get("q")

    products = (Product.objects.all()
                .select_related("category")
                .select_related("supplier")
                .select_related("producer")
                .select_related("measure_unit"))

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, "search.html", { "products": products })


def login_view(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        login_input = request.POST.get("login")
        password = request.POST.get("password")

        user = authenticate(request, username=login_input, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html",
                          {"error": "Неверный логин или пароль."})

    return render(request, "login.html")


def logout_view(request):

    logout(request)
    request.session["redirected_to_login"] = True

    return redirect("login")
