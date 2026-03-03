"""
URL configuration for dem_exam_practice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shoes_market import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('search/', views.search_view, name="search"),
    path('add_product/', views.add_edit_product_view, name="add_product"),
    path('edit_product/<str:product_article>', views.add_edit_product_view, name="edit_product"),
    path('delete_product/<str:product_article>', views.delete_product_view, name="delete_product"),
    path('orders/', views.orders_view, name="orders"),
    path('add_order/', views.add_edit_order_view, name="add_order"),
    path('edit_order/<int:product_in_order_id>', views.add_edit_order_view, name="edit_order"),
    path('delete_order/<int:product_in_order_id>', views.delete_order_view, name="delete_order")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
