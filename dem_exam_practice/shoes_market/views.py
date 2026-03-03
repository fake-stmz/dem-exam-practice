from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Product, Supplier, Category, Producer, MeasureUnit, ProductInOrder, Status, PickupPoint, Order


def index(request):

    if not request.session.get("redirected_to_login", False):
        request.session["redirected_to_login"] = True
        return redirect("login")

    suppliers = Supplier.objects.all()

    context = {
        "suppliers": suppliers
    }

    current_user = request.user

    if current_user.groups.filter(name="Авторизированный клиент").exists():
        return render(request, "index_client.html")

    if current_user.groups.filter(name="Менеджер").exists():
        return render(request, "index_manager.html", context)

    if current_user.groups.filter(name="Администратор").exists():
        return render(request, "index_admin.html", context)

    return render(request, "index.html")


def search_view(request):

    search_query = request.GET.get("q")
    quantity_sorting = request.GET.get("sort")
    supplier_filter = request.GET.get("filter")

    products = get_filtered_products(search_query, quantity_sorting, supplier_filter)

    is_admin = True if request.user.groups.filter(name="Администратор").exists() else False

    return render(request, "search.html", { "products": products, "is_admin": is_admin })


def get_filtered_products(search_query='', quantity_sorting='', supplier_filter=None):
    products = (Product.objects.all()
                .select_related("category","supplier", "producer", "measure_unit"))

    if quantity_sorting == 'asc':
        products = products.order_by("quantity")
    else:
        products = products.order_by("-quantity")

    if supplier_filter:
        products = products.filter(supplier_id=supplier_filter)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(supplier__name__icontains=search_query) |
            Q(producer__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    return products


def add_edit_product_view(request, product_article = None):

    if not request.user.groups.filter(name="Администратор").exists():
        redirect('index')

    categories = Category.objects.all()
    measure_units = MeasureUnit.objects.all()
    producers = Producer.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        new_product = Product() if not product_article else Product.objects.get(article=product_article)
        new_product.article = request.POST.get("article")
        new_product.name = request.POST.get("name")
        new_product.price = request.POST.get("price")
        new_product.discount = request.POST.get("discount")
        new_product.quantity = request.POST.get("quantity")
        new_product.description = request.POST.get("description")
        new_product.category = Category.objects.get(id=request.POST.get("category"))
        new_product.measure_unit = MeasureUnit.objects.get(id=request.POST.get("mes_unit"))
        new_product.producer = Producer.objects.get(id=request.POST.get("producer"))
        new_product.supplier = Supplier.objects.get(id=request.POST.get("supplier"))

        photo_file = request.FILES.get("photo")
        if photo_file:
            new_product.picture = photo_file

        new_product.save()

        return redirect("index")


    context = {
        "categories": categories,
        "measure_units": measure_units,
        "producers": producers,
        "suppliers": suppliers,
    }

    if product_article:
        context["product"] = Product.objects.get(article=product_article)

    return render(request, "add_edit.html", context)


def delete_product_view(request, product_article):

    if not request.user.groups.filter(name="Администратор").exists():
        redirect('index')

    product = Product.objects.get(article=product_article)
    product.delete()

    return redirect("index")


def orders_view(request):

    orders = ProductInOrder.objects.all().select_related("order", "product").order_by("-order__order_date")

    context = {
        "orders": orders
    }

    if request.user.groups.filter(name="Администратор").exists():
        return render(request, "orders_admin.html", context)
    elif request.user.groups.filter(name="Менеджер").exists():
        return render(request, "orders.html", context)
    else:
        return redirect("index")


def add_edit_order_view(request, product_in_order_id = None):

    if not request.user.groups.filter(name="Администратор").exists():
        redirect('index')

    products = Product.objects.all()
    statuses = Status.objects.all()
    pickup_points = PickupPoint.objects.all()
    clients = User.objects.all()

    if request.method == "POST":
        new_product_in_order = ProductInOrder() if not product_in_order_id else ProductInOrder.objects.get(id=product_in_order_id)

        new_order = Order() if not product_in_order_id else new_product_in_order.order
        new_order.order_date = request.POST.get("order_date")
        new_order.delivery_date = request.POST.get("delivery_date")
        new_order.pickup_point = PickupPoint.objects.get(id=request.POST.get("pickup_point"))
        new_order.client = User.objects.get(id=request.POST.get("client"))
        new_order.receive_code = request.POST.get("receive_code")
        new_order.status = Status.objects.get(id=request.POST.get("status"))

        new_order.save()

        new_product_in_order.product = Product.objects.get(article=request.POST.get("article"))
        new_product_in_order.order = new_order
        new_product_in_order.quantity = request.POST.get("quantity")

        new_product_in_order.save()

        return redirect("orders")

    context = {
        "products": products,
        "statuses": statuses,
        "pickup_points": pickup_points,
        "clients": clients
    }

    if product_in_order_id:
        context["order"] = ProductInOrder.objects.get(id=product_in_order_id)

    return render(request, "add_edit_order.html", context)


def delete_order_view(request, product_in_order_id):

    if not request.user.groups.filter(name="Администратор").exists():
        redirect('index')

    product_in_order = ProductInOrder.objects.get(id=product_in_order_id)
    order = product_in_order.order

    product_in_order.delete()

    if order.product_in_order.count() == 0:
        order.delete()

    return redirect("orders")



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
