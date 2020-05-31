from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("<int:menuitem_id>", views.item_view, name="item"),
    path("<int:menuitem_id>/add_to_cart",
         views.add_to_cart, name="add_to_cart"),
    path("<user>/mycart", views.cart_view, name="mycart"),
    path("<user>/checkout", views.checkout, name="checkout"),
    path("<user>/order", views.order, name="order"),
    path("manager", views.manager_view, name="manager"),
]
